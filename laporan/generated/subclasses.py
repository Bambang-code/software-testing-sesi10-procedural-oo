class FoodSellerApplication(SellerApplication):
    """Mewarisi seluruh aturan transisi, mengkhususkan label kategori."""

    def category(self) -> str:
        return "FOOD"

class ClothingSellerApplication(SellerApplication):
    """Mewarisi seluruh aturan transisi, mengkhususkan label kategori."""

    def category(self) -> str:
        return "CLOTHING"
