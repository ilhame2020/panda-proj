# Mapping des codes de remise vers un taux de remise

def apply_discount(data, discount_mapping,tva=0.2):
    """
    Applique les remises et calcule le montant net et la taxe.
    """
    
    # Calculer le taux de remise à partir du code
    data["discount_rate"] = data["discount_code"].map(discount_mapping).fillna(0.0)
    
    # Montant de la remise
    data["discount_amount"] = data["total_amount"] * data["discount_rate"]
    
    # Montant net
    data["net_amount"] = data["total_amount"] - data["discount_amount"]
    
    # Taxe (exemple TVA 20%)
    data["tax"] = data["net_amount"] * tva
    
    return data


