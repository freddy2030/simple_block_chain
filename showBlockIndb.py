from leveldbapi import mleveldb as db

print(db.getValue("4f025c4ef95f64c069dc448b3aef548332f0db12ef7567ff8fa345bd16fe8f11"))
print(db.getValue("chain_info"))