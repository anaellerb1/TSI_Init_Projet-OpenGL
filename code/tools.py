import OpenGL.GL as GL
import glfw
import numpy as np
import os
from ctypes import sizeof, c_float, c_void_p

def compile_shader(shader_content, shader_type):
        # compilation d'un shader donné selon son type
        # un shader sert à décrire un effet graphique
        shader_id = GL.glCreateShader(shader_type)
        GL.glShaderSource(shader_id, shader_content)
        GL.glCompileShader(shader_id)

        success = GL.glGetShaderiv(shader_id, GL.GL_COMPILE_STATUS)
        if not success:
            log = GL.glGetShaderInfoLog(shader_id).decode('ascii')
            print(f'{25*"-"}\nError compiling shader: \n{shader_content}\n{5*"-"}\n{log}\n{25*"-"}')
        return shader_id

def create_program(vertex_source, fragment_source):
    # création d'un programme GPU
    vs_id = compile_shader(vertex_source, GL.GL_VERTEX_SHADER)
    fs_id = compile_shader(fragment_source, GL.GL_FRAGMENT_SHADER)

    if vs_id and fs_id:
        program_id = GL.glCreateProgram()
        GL.glAttachShader(program_id, vs_id)
        GL.glAttachShader(program_id, fs_id)
        GL.glLinkProgram(program_id)

        success = GL.glGetProgramiv(program_id, GL.GL_LINK_STATUS)
        if not success:
            log = GL.glGetProgramInfoLog(program_id).decode('ascii')
            print(f'{25*"-"}\nError linking program:\n{log}\n{25*"-"}')

        GL.glDeleteShader(vs_id)
        GL.glDeleteShader(fs_id)

        return program_id

def create_program_from_file(vs_file, fs_file):
    # création d'un programme GPU à partir de fichiers
    vs_content = open(vs_file, 'r',  encoding='utf-8').read() if os.path.exists(vs_file) \
        else print(f'{25*"-"}\nError reading file:\n{vs_file}\n{25*"-"}')

    fs_content = open(fs_file, 'r', encoding='utf-8').read() if os.path.exists(fs_file) \
        else print(f'{25*"-"}\nError reading file:\n{fs_file}\n{25*"-"}')

    return create_program(vs_content, fs_content)

def config_shape(sommets, indices, program, forme):
    """
    Configure une forme 3D en créant et liant le VAO, VBO et EBO.
    Attribue les attributs de sommets (position, normale, couleur, UV),
    en fonction de la forme indiquée (cube, plan, sphère...).

    Paramètres :
        sommets : np.array des sommets
        indices : np.array des indices
        program : programme OpenGL (shader actif)
        forme : str, nom de la forme (ex : 'cube', 'plan', 'sphere')

    Retourne :
        vao : identifiant du VAO
        nb_indices : nombre d’indices (entiers)
    """
    # Création du VAO : pour les attributs de sommets (positions, normales, couleurs, UV)
    vao = GL.glGenVertexArrays(1)  # Génération d'un VAO
    GL.glBindVertexArray(vao)     # On lie le VAO pour l'utiliser

    # Création du VBO : pour les sommets
    vbo = GL.glGenBuffers(1) 
    GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
    GL.glBufferData(GL.GL_ARRAY_BUFFER, sommets.nbytes, sommets, GL.GL_STATIC_DRAW)

    # Création de l'EBO (Element Buffer Object = indices)
    ebo = GL.glGenBuffers(1)
    GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, ebo)
    GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL.GL_STATIC_DRAW)

    # Définition du format en fonction de la forme
    if forme == 'cube' or forme == 'plan':
        attributs = [
            ("position", 3),
            ("normale", 3),
            ("couleur", 3),
            ("uv", 2)
        ]
    elif forme == 'sphere':
        attributs = [
            ("position", 3),
            ("normale", 3),
            ("uv", 2)
        ]
    else:
        raise ValueError(f"[Erreur] Forme non reconnue : '{forme}'")

    octets_par_sommet = sommets.strides[0]
    offset = 0

    # Activation des attributs déclarés
    for nom, taille in attributs:
        location = GL.glGetAttribLocation(program, nom)
        if location != -1:
            GL.glVertexAttribPointer(location, taille, GL.GL_FLOAT, GL.GL_FALSE, octets_par_sommet, c_void_p(offset))
            GL.glEnableVertexAttribArray(location)
        offset += taille * sizeof(c_float)

    return vao, len(indices)
