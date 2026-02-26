from app.repositories.products import ProductRepository


class ProductService:
    def __init__(self, repo: ProductRepository): self.repo=repo
