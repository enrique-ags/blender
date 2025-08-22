import bpy
import math

# --- PARÁMETROS ---
DRILL_DIAMETER = 8 # ¡Ajustado a 8 unidades para el diámetro!
DRILL_LENGTH = 100
FLUTE_TWIST_COUNT = 4
FLUTE_WIDTH_RATIO = 0.4
FLUTE_DEPTH_RATIO = 0.3
FLUTE_COUNT = 2

# --- FUNCIÓN DE AYUDA ---
def clean_scene():
    """Limpia la escena para empezar desde cero."""
    if bpy.context.mode == 'EDIT_MESH':
        bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

# --- FUNCIÓN DE EJECUCIÓN PRINCIPAL ---
def create_drill_bit():
    clean_scene()
    
    # 1. Crear el cuerpo cilíndrico de la broca
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=64,
        radius=DRILL_DIAMETER / 2 * (1 - FLUTE_DEPTH_RATIO),
        depth=DRILL_LENGTH,
        location=(0, 0, DRILL_LENGTH / 2)
    )
    core = bpy.context.object
    
    # 2. Crear las hélices de corte
    helix_vertices = []
    helix_faces = []
    
    num_segments = 100
    segment_length = DRILL_LENGTH / num_segments
    radius_outer = DRILL_DIAMETER / 2
    radius_inner = DRILL_DIAMETER / 2 * (1 - FLUTE_WIDTH_RATIO)
    
    for i in range(FLUTE_COUNT):
        offset = i * (2 * math.pi / FLUTE_COUNT)
        for j in range(num_segments + 1):
            z = j * segment_length
            angle = (z / DRILL_LENGTH) * (2 * math.pi * FLUTE_TWIST_COUNT) + offset
            
            # Vértices exteriores
            x_outer = radius_outer * math.cos(angle)
            y_outer = radius_outer * math.sin(angle)
            helix_vertices.append((x_outer, y_outer, z))
            
            # Vértices interiores
            x_inner = radius_inner * math.cos(angle)
            y_inner = radius_inner * math.sin(angle)
            helix_vertices.append((x_inner, y_inner, z))
            
    # Conectar los vértices con caras
    vertex_count = len(helix_vertices)
    for i in range(0, vertex_count - 2, 2):
        v1 = i
        v2 = i + 1
        v3 = i + 3
        v4 = i + 2
        
        if v4 < vertex_count:
            helix_faces.append([v1, v2, v3, v4])
    
    # Crear el objeto de la hélice
    mesh_data = bpy.data.meshes.new("Helix_Mesh")
    mesh_data.from_pydata(helix_vertices, [], helix_faces)
    mesh_data.update()
    
    helix_object = bpy.data.objects.new("Helix", mesh_data)
    bpy.context.collection.objects.link(helix_object)
    
    # 3. Unir el núcleo y las hélices en un solo objeto
    bpy.ops.object.select_all(action='DESELECT')
    core.select_set(True)
    helix_object.select_set(True)
    bpy.context.view_layer.objects.active = core
    bpy.ops.object.join()
    
    print("Modelo de broca generado con éxito!")

# Ejecutar el script
if __name__ == "__main__":
    create_drill_bit()
