"""Thread-safe capability catalogue with deterministic selection."""
from __future__ import annotations

from threading import RLock
from typing import Iterable

from .contracts import CapabilityRequirement, ModelCapabilities
from .errors import DuplicateModelError, ModelNotFoundError


class CapabilityRegistry:
    """In-memory registry. Registration is explicit; there is no name-based guessing."""

    def __init__(self, models: Iterable[ModelCapabilities] = ()) -> None:
        self._lock = RLock()
        self._models: dict[str, ModelCapabilities] = {}
        self.register_many(models)

    def register(self, item: ModelCapabilities, *, replace: bool = False) -> None:
        self.register_many((item,), replace=replace)

    def register_many(self, items: Iterable[ModelCapabilities], *, replace: bool = False) -> None:
        """Validate the whole batch before mutating, so a bad batch is atomic."""
        batch = tuple(items)
        if any(not isinstance(item, ModelCapabilities) for item in batch):
            raise TypeError("all registry entries must be ModelCapabilities")
        ids = [item.model_id for item in batch]
        if len(ids) != len(set(ids)):
            raise DuplicateModelError("batch contains duplicate model IDs")
        with self._lock:
            conflicts = set(ids).intersection(self._models)
            if conflicts and not replace:
                raise DuplicateModelError(f"models already registered: {', '.join(sorted(conflicts))}")
            updated = dict(self._models)
            updated.update((item.model_id, item) for item in batch)
            self._models = updated

    def get(self, model_id: str) -> ModelCapabilities:
        with self._lock:
            try:
                return self._models[model_id]
            except KeyError as exc:
                raise ModelNotFoundError(model_id) from exc

    def remove(self, model_id: str) -> ModelCapabilities:
        with self._lock:
            try:
                return self._models.pop(model_id)
            except KeyError as exc:
                raise ModelNotFoundError(model_id) from exc

    def list_models(self) -> tuple[ModelCapabilities, ...]:
        with self._lock:
            return tuple(self._models[key] for key in sorted(self._models))

    def select(self, requirement: CapabilityRequirement) -> tuple[ModelCapabilities, ...]:
        if not isinstance(requirement, CapabilityRequirement):
            raise TypeError("requirement must be CapabilityRequirement")
        with self._lock:
            candidates = tuple(self._models.values())
        matches = [
            model for model in candidates
            if (requirement.provider is None or requirement.provider in model.providers)
            and requirement.required_capabilities.issubset(model.capabilities)
            and requirement.required_input_modalities.issubset(model.input_modalities)
            and requirement.required_output_modalities.issubset(model.output_modalities)
            and model.context_tokens >= requirement.min_context_tokens
            and model.max_output_tokens >= requirement.min_output_tokens
        ]
        # Prefer the smallest model that satisfies the request only if the caller
        # can supply a cost signal; absent that, maximize usable context/output.
        return tuple(sorted(matches, key=lambda m: (-m.context_tokens, -m.max_output_tokens, m.model_id)))

    def resolve(self, model_id: str, provider: str) -> tuple[ModelCapabilities, str]:
        """Resolve canonical identity to the concrete provider model identifier."""
        model = self.get(model_id)
        return model, model.provider_model_id(provider)

    def __len__(self) -> int:
        with self._lock:
            return len(self._models)
