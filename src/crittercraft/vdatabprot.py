# src/crittercraft/vdatabprot.py

# Import the real, powerful ROL from our other project
from vdatabprot_v2.rol import write as vdb_write
from vdatabprot_v2.rol import read as vdb_read

def save(pet_id, pet_data):
    """Saves pet data using the REAL VDataBProt ROL."""
    # The ROL needs bytes, so we must serialize our object.
    import pickle
    data_bytes = pickle.dumps(pet_data)
    vdb_write(pet_id, data_bytes)

def load(pet_id):
    """Loads pet data using the REAL VDataBProt ROL."""
    import pickle
    data_bytes = vdb_read(pet_id)
    if data_bytes:
        return pickle.loads(data_bytes)
    return None
