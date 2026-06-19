import pandas as pd

df = pd.read_csv("claims.csv")

outputs = []

def extract_claim(text):
    text = str(text).lower()

    issue_type = "unknown"
    object_part = "unknown"

    if "dent" in text:
        issue_type = "dent"
    elif "scratch" in text:
        issue_type = "scratch"
    elif "crack" in text or "cracked" in text:
        issue_type = "crack"
    elif "broken" in text:
        issue_type = "broken_part"
    elif "crushed" in text:
        issue_type = "crushed"
    elif "water" in text or "stain" in text:
        issue_type = "water_damage"

    parts = [
        "bumper","door","screen","keyboard","hinge",
        "trackpad","windshield","mirror","headlight",
        "taillight","hood","package","seal","label","corner"
    ]

    for p in parts:
        if p in text:
            object_part = p

    return issue_type, object_part


def get_images(image_paths):
    return str(image_paths).split(";")


for i, row in df.iterrows():

    claim_text = row["user_claim"]
    images = get_images(row["image_paths"])

    issue_type, object_part = extract_claim(claim_text)

    outputs.append({
        "user_id": row["user_id"],
        "issue_type": issue_type,
        "object_part": object_part,
        "claim_status": "supported",
        "severity": "medium",
        "risk_flags": "none",
        "supporting_image_ids": row["image_paths"],
        "valid_image": True,
        "claim_status_justification": "baseline submission"
    })

out_df = pd.DataFrame(outputs)
out_df.to_csv("output.csv", index=False)

print("DONE → output.csv generated")
