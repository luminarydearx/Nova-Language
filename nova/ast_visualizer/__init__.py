"""
AST Visualizer untuk Nova Language
Mengubah AST menjadi representasi teks (ASCII tree) atau JSON
"""

def ast_to_dict(node) -> dict:
    """Ubah AST node menjadi dictionary (JSON-serializable)"""
    if node is None:
        return None
    
    # Dapatkan nama kelas
    class_name = type(node).__name__
    
    # Atribut yang akan di-serialize (field dari dataclass)
    attrs = {}
    for field in node.__dataclass_fields__:
        value = getattr(node, field.name)
        
        # Rekursif untuk node anak
        if isinstance(value, list):
            attrs[field.name] = [_serialize_item(item) for item in value]
        else:
            attrs[field.name] = _serialize_item(value)
    
    return {
        "type": class_name,
        "attributes": attrs
    }

def _serialize_item(item):
    """Serializer untuk item tunggal"""
    if hasattr(item, '__dataclass_fields__'):  # Cek apakah dataclass
        return ast_to_dict(item)
    elif isinstance(item, list):
        return [ast_to_dict(i) for i in item]
    elif isinstance(item, (str, int, float, bool, type(None))):
        return item
    else:
        return str(item)  # Fallback buat tipe lain

def print_ast(node, indent: int = 0, output: list = None) -> str:
    """Cetak AST sebagai pohon ASCII"""
    if output is None:
        output = []
    
    prefix = "  " * indent
    class_name = type(node).__name__
    
    if hasattr(node, '__dataclass_fields__'):
        output.append(f"{prefix}{class_name}(")
        for field in node.__dataclass_fields__.values():
            value = getattr(node, field.name)
            if isinstance(value, list):
                output.append(f"{prefix}  {field.name}: [")
                for item in value:
                    print_ast(item, indent + 2, output)
                output.append(f"{prefix}  ]")
            elif hasattr(value, '__dataclass_fields__'):
                output.append(f"{prefix}  {field.name}: ")
                print_ast(value, indent + 2, output)
            else:
                output.append(f"{prefix}  {field.name}: {repr(value)}")
        output.append(f"{prefix})")
    else:
        output.append(f"{prefix}{repr(node)}")
    
    if indent == 0:
        return "\n".join(output)
    return output
