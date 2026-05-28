import bpy
import math

def clear_scene():
    """Очищает сцену от всех объектов"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def create_house():
    """Создает модель простого домика"""
    
    # Очищаем сцену
    clear_scene()
    
    # 0. Создаем фундамент (платформа) на точной высоте
    bpy.ops.mesh.primitive_cube_add(
        size=1,
        location=(0, 0, -0.332839)
    )
    foundation = bpy.context.active_object
    foundation.name = "Foundation"
    foundation.scale = (3.4, 3.4, 0.1)
    
    # Материал для фундамента (бетон/камень)
    foundation_material = bpy.data.materials.new(name="Foundation_Material")
    foundation_material.use_nodes = True
    foundation_material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.6, 0.6, 0.65, 1)
    foundation_material.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0.8
    foundation.data.materials.append(foundation_material)
    
    # 1. Создаем основание дома
    bpy.ops.mesh.primitive_cube_add(
        size=1, 
        location=(0, 0, 0.6)
    )
    house_body = bpy.context.active_object
    house_body.name = "House_Body"
    house_body.scale = (3, 3, 1.8)
    
    # Материал для стен (дерево)
    wall_material = bpy.data.materials.new(name="Wall_Material")
    wall_material.use_nodes = True
    wall_material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.85, 0.75, 0.65, 1)
    wall_material.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0.3
    house_body.data.materials.append(wall_material)
    
    # 2. Создаем крышу на точной высоте
    bpy.ops.mesh.primitive_cone_add(
        vertices=4,
        radius1=2.15,
        radius2=0,
        depth=1.4,
        location=(0, 0, 2.19618)
    )
    roof = bpy.context.active_object
    roof.name = "House_Roof"
    roof.rotation_euler = (0, 0, math.radians(45))
    
    # Материал для крыши (красная черепица)
    roof_material = bpy.data.materials.new(name="Roof_Material")
    roof_material.use_nodes = True
    roof_material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.7, 0.2, 0.15, 1)
    roof_material.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0.6
    roof.data.materials.append(roof_material)
    
    # 3. Создаем трубу на точных координатах
    bpy.ops.mesh.primitive_cube_add(
        size=0.5, 
        location=(0.946915, 0.602718, 2.07389)
    )
    chimney = bpy.context.active_object
    chimney.name = "Chimney"
    chimney.scale = (1, 1, 1.5)
    
    # Материал для трубы (кирпич)
    chimney_material = bpy.data.materials.new(name="Chimney_Material")
    chimney_material.use_nodes = True
    chimney_material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.55, 0.3, 0.2, 1)
    chimney_material.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0.7
    chimney.data.materials.append(chimney_material)
    
    # 4. Создаем дверь
    bpy.ops.mesh.primitive_cube_add(
        size=0.5,
        location=(0, -1.51, 0.5)
    )
    door = bpy.context.active_object
    door.name = "Door"
    door.scale = (0.8, 0.1, 1.3)
    
    # Материал для двери (темное дерево)
    door_material = bpy.data.materials.new(name="Door_Material")
    door_material.use_nodes = True
    door_material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.3, 0.15, 0.05, 1)
    door_material.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0.4
    door.data.materials.append(door_material)
    
    # 5. Создаем окно (слева от двери)
    bpy.ops.mesh.primitive_cube_add(
        size=0.5,
        location=(-1.2, -1.51, 1.0)
    )
    window1 = bpy.context.active_object
    window1.name = "Window_Left"
    window1.scale = (0.9, 0.1, 0.9)
    
    # 6. Создаем второе окно (справа от двери)
    bpy.ops.mesh.primitive_cube_add(
        size=0.5,
        location=(1.2, -1.51, 1.0)
    )
    window2 = bpy.context.active_object
    window2.name = "Window_Right"
    window2.scale = (0.9, 0.1, 0.9)
    
    # 7. Создаем окно на задней стене
    bpy.ops.mesh.primitive_cube_add(
        size=0.5,
        location=(0, 1.51, 1.0)
    )
    window_back = bpy.context.active_object
    window_back.name = "Window_Back"
    window_back.scale = (0.9, 0.1, 0.9)
    
    # 8. Создаем окно на левой боковой стене
    bpy.ops.mesh.primitive_cube_add(
        size=0.5,
        location=(-1.51, -0.8, 1.0)
    )
    window_side_left = bpy.context.active_object
    window_side_left.name = "Window_Side_Left"
    window_side_left.scale = (0.1, 0.9, 0.9)
    
    # Материал для окон (стекло)
    window_material = bpy.data.materials.new(name="Window_Material")
    window_material.use_nodes = True
    window_material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.6, 0.8, 0.95, 1)
    window_material.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0.2
    window_material.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 0.8
    window1.data.materials.append(window_material)
    window2.data.materials.append(window_material)
    window_back.data.materials.append(window_material)
    window_side_left.data.materials.append(window_material)
    
    # Материал для рам (дерево)
    wood_material = bpy.data.materials.new(name="Wood_Material")
    wood_material.use_nodes = True
    wood_material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.5, 0.35, 0.2, 1)
    wood_material.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0.5
    
    # Добавляем рамы для передних окон
    for window_obj in [window1, window2, window_back]:
        # Горизонтальная перекладина
        bpy.ops.mesh.primitive_cube_add(
            size=0.05,
            location=(window_obj.location.x, window_obj.location.y, window_obj.location.z)
        )
        frame_h = bpy.context.active_object
        frame_h.name = f"{window_obj.name}_Frame_H"
        frame_h.scale = (1.8, 0.05, 0.05)
        frame_h.data.materials.append(wood_material)
        
        # Вертикальная перекладина
        bpy.ops.mesh.primitive_cube_add(
            size=0.05,
            location=(window_obj.location.x, window_obj.location.y, window_obj.location.z)
        )
        frame_v = bpy.context.active_object
        frame_v.name = f"{window_obj.name}_Frame_V"
        frame_v.scale = (0.05, 0.05, 1.8)
        frame_v.data.materials.append(wood_material)
    
    # Рама для бокового окна
    bpy.ops.mesh.primitive_cube_add(
        size=0.05,
        location=(window_side_left.location.x, window_side_left.location.y, window_side_left.location.z)
    )
    frame_h_side = bpy.context.active_object
    frame_h_side.name = "Window_Side_Left_Frame_H"
    frame_h_side.scale = (0.05, 1.5, 0.05)
    frame_h_side.data.materials.append(wood_material)
    
    bpy.ops.mesh.primitive_cube_add(
        size=0.05,
        location=(window_side_left.location.x, window_side_left.location.y, window_side_left.location.z)
    )
    frame_v_side = bpy.context.active_object
    frame_v_side.name = "Window_Side_Left_Frame_V"
    frame_v_side.scale = (0.05, 0.05, 1.5)
    frame_v_side.data.materials.append(wood_material)
    
    # Добавляем наличники на дверь
    door_trim_material = bpy.data.materials.new(name="Door_Trim_Material")
    door_trim_material.use_nodes = True
    door_trim_material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.7, 0.6, 0.5, 1)
    
    # Левая сторона наличника
    bpy.ops.mesh.primitive_cube_add(
        size=0.05,
        location=(-0.45, -1.5, 0.65)
    )
    door_trim_left = bpy.context.active_object
    door_trim_left.name = "Door_Trim_Left"
    door_trim_left.scale = (0.05, 0.05, 1.4)
    door_trim_left.data.materials.append(door_trim_material)
    
    # Правая сторона наличника
    bpy.ops.mesh.primitive_cube_add(
        size=0.05,
        location=(0.45, -1.5, 0.65)
    )
    door_trim_right = bpy.context.active_object
    door_trim_right.name = "Door_Trim_Right"
    door_trim_right.scale = (0.05, 0.05, 1.4)
    door_trim_right.data.materials.append(door_trim_material)
    
    # Верхняя часть наличника
    bpy.ops.mesh.primitive_cube_add(
        size=0.05,
        location=(0, -1.5, 1.35)
    )
    door_trim_top = bpy.context.active_object
    door_trim_top.name = "Door_Trim_Top"
    door_trim_top.scale = (1.0, 0.05, 0.05)
    door_trim_top.data.materials.append(door_trim_material)
    
    # Выбираем все объекты для объединения
    bpy.ops.object.select_all(action='DESELECT')
    
    # Выбираем все созданные объекты
    all_objects = [foundation, house_body, roof, chimney, door, window1, window2, 
                   window_back, window_side_left, door_trim_left, door_trim_right, door_trim_top]
    
    # Добавляем рамки окон
    for obj in bpy.data.objects:
        if "Frame" in obj.name:
            all_objects.append(obj)
    
    # Выделяем все объекты
    for obj in all_objects:
        obj.select_set(True)
    
    # Делаем один из объектов активным
    bpy.context.view_layer.objects.active = house_body
    
    # Объединяем все объекты в один
    bpy.ops.object.join()
    
    # Переименовываем объединенный объект
    merged_house = bpy.context.active_object
    merged_house.name = "House"
    bpy.ops.wm.obj_export(filepath="./object.obj")
    
    print("Домик успешно создан и объединен в один объект!")
    print(f"Крыша на высоте: 2.19618 m")
    print(f"Фундамент на высоте: -0.332839 m")
    print(f"Труба на координатах: 0.946915, 0.602718, 2.07389")
    return merged_house


house = create_house()
    
print("Скрипт завершен! Домик готов к просмотру.")
