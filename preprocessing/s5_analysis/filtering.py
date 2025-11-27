#(Q13–Q16)
def filter_quantity_gt_3(df):
    return df[df["quantity"] > 3]


def filter_total_amount_gt_1000(df):
    return df[df["total_amount"] > 1000]


def filter_region_casa_settat(df):
    return df[df["region"] == "Casablanca-Settat"]


def filter_not_cash(df):
    return df[df["payment_method"] != "Cash on Delivery"]
