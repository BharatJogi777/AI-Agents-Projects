"""Create product catalogue entries from supplied image labels and metadata."""
from dataclasses import dataclass
@dataclass(frozen=True)
class ProductImage:
    image_ref:str
    sku:str
    title:str
    category:str
    tags:tuple[str,...]
def create_catalog_entry(p:ProductImage,known_skus:set[str])->dict:
    if not all(x.strip() for x in (p.image_ref,p.sku,p.title,p.category)): raise ValueError("image reference, SKU, title, and category are required")
    if p.sku in known_skus: raise ValueError("SKU already exists")
    if any(not t.strip() for t in p.tags): raise ValueError("tags cannot be blank")
    return {"image_ref":p.image_ref,"sku":p.sku,"title":p.title,"category":p.category,"tags":list(dict.fromkeys(t.casefold().strip() for t in p.tags)),
            "published":False,"human_review_required":True}
