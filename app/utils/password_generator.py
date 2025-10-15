# app/utils/password_generator.py
def generate_password_from_user_data(name: str, last_name: str, identification: str) -> str:
    """
    Genera password: primera letra nombre + primera palabra apellido + últimos 4 dígitos RUT
    Ejemplo: Juan Pérez González, 12345678-9 → JPer5678
    """
    # Primera letra del nombre en mayúscula
    first_letter = name.strip()[0].upper() if name and name.strip() else ""
    
    # Primera palabra del apellido capitalizada
    last_name_parts = last_name.strip().split() if last_name else []
    first_lastname = last_name_parts[0].capitalize() if last_name_parts else ""
    
    # Últimos 4 dígitos del RUT/identificación
    digits_only = ''.join(filter(str.isdigit, identification)) if identification else ""
    last_four = digits_only[-4:] if len(digits_only) >= 4 else digits_only
    
    password = f"{first_letter}{first_lastname}{last_four}"
    
    return password if len(password) > 3 else "TempPass123"
