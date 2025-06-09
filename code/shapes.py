### shapes.py

import numpy as np

def get_plane():
    """
    Renvoie les données d’un plan simple sur l’axe Z.

    Retourne :
        sommets : tableau numpy (float32)
        indices : tableau numpy (uint32)
    """
    # Sommets (positions)
    p0 = (-0.5, -0.5, 0)
    p1 = ( 0.5, -0.5, 0)
    p2 = ( 0.5,  0.5, 0)
    p3 = (-0.5,  0.5, 0)

    # Normales
    n0 = (0, 0, 1) # Normale pour le plan sur l'axe Z
    n1 = (0, 0, 1) # Normale pour le plan sur l'axe Z
    n2 = (0, 0, 1) # Normale pour le plan sur l'axe Z
    n3 = (0, 0, 1) # Normale pour le plan sur l'axe Z

    # Couleurs 
    c0 = (1, 0, 0) # Rouge
    c1 = (0, 1, 0) # Vert
    c2 = (0, 0, 1) # Bleu
    c3 = (1, 1, 0) # Jaune

    # Coordonnées UV
    uv0 = (0, 0) # Coordonn´ees de texture pour le coin inférieur gauche
    uv1 = (1, 0) # Coordonn´ees de texture pour le coin inférieur droit
    uv2 = (1, 1) # Coordonn´ees de texture pour le coin supérieur droit
    uv3 = (0, 1) # Coordonn´ees de texture pour le coin supérieur gauche
        
    # Sommets du plan
    
    sommets = np.array([
        *p0, *n0, *c0, *uv0,
        *p1, *n1, *c1, *uv1,
        *p2, *n2, *c2, *uv2,
        *p3, *n3, *c3, *uv3
    ], dtype=np.float32)
    

    # Faces du plan
    f0 = (0, 1, 2) # Triangle inférieur droit
    f1 = (0, 2, 3) # Triangle supérieur gauche

    # Indices 
    indices = np.array([*f0, *f1], dtype=np.uint32)


    return sommets, indices

def get_cube():
    """
    Renvoie les données d’un cube simple.

    Retourne :
        sommets : tableau numpy (float32)
        indices : tableau numpy (uint32)
    """    
    # Face avant (z = 1), couleur rouge :
    p0 = (0, 0, 1)
    p1 = (1, 0, 1)
    p2 = (1, 1, 1)
    p3 = (0, 1, 1)

    n0 = (0, 0, 1)
    n1 = (0, 0, 1)
    n2 = (0, 0, 1)
    n3 = (0, 0, 1)

    c0 = (1, 0, 0) # Rouge
    c1 = (1, 0, 0)
    c2 = (1, 0, 0)
    c3 = (1, 0, 0)

    uv0 = (0, 0)
    uv1 = (1, 0)
    uv2 = (1, 1)
    uv3 = (0, 1)

    # Face arrière (z = 0), couleur vert :
    p4 = (1, 0, 0)
    p5 = (0, 0, 0)
    p6 = (0, 1, 0)
    p7 = (1, 1, 0)

    n4 = (0, 0, -1)
    n5 = (0, 0, -1)
    n6 = (0, 0, -1)
    n7 = (0, 0, -1)

    c4 = (0, 1, 0) # Vert
    c5 = (0, 1, 0)
    c6 = (0, 1, 0)
    c7 = (0, 1, 0)

    uv4 = (0, 0)
    uv5 = (1, 0)
    uv6 = (1, 1)
    uv7 = (0, 1)

    # Face droite (x = 1), couleur bleu :
    p8 = (1, 0, 1)
    p9 = (1, 0, 0)
    p10 = (1, 1, 0)
    p11 = (1, 1, 1)

    n8 = (1, 0, 0)
    n9 = (1, 0, 0)
    n10 = (1, 0, 0)
    n11 = (1, 0, 0)

    c8 = (0, 0, 1) # Bleu
    c9 = (0, 0, 1)
    c10 = (0, 0, 1)
    c11 = (0, 0, 1)

    uv8 = (0, 0)
    uv9 = (1, 0)
    uv10 = (1, 1)
    uv11 = (0, 1)

    #Face gauche (x = 0), couleur jaune :
    p12 = (0, 0, 0)
    p13 = (0, 0, 1)
    p14 = (0, 1, 1)
    p15 = (0, 1, 0)

    n12 = (-1, 0, 0)
    n13 = (-1, 0, 0)
    n14 = (-1, 0, 0)
    n15 = (-1, 0, 0)

    c12 = (1, 1, 0) # Jaune
    c13 = (1, 1, 0)
    c14 = (1, 1, 0)
    c15 = (1, 1, 0)

    uv12 = (0, 0)
    uv13 = (1, 0)
    uv14 = (1, 1)
    uv15 = (0, 1)

    #Face supérieure (y = 1), couleur cyan :
    p16 = (0, 1, 1)
    p17 = (1, 1, 1)
    p18 = (1, 1, 0)
    p19 = (0, 1, 0)

    n16 = (0, 1, 0)
    n17 = (0, 1, 0)
    n18 = (0, 1, 0)
    n19 = (0, 1, 0)

    c16 = (0, 1, 1) # Cyan
    c17 = (0, 1, 1)
    c18 = (0, 1, 1)
    c19 = (0, 1, 1)

    uv16 = (0, 0)
    uv17 = (1, 0)
    uv18 = (1, 1)
    uv19 = (0, 1)

    #Face inférieure (y = 0), couleur magenta :
    p20 = (0, 0, 0)
    p21 = (1, 0, 0)
    p22 = (1, 0, 1)
    p23 = (0, 0, 1)

    n20 = (0, -1, 0)
    n21 = (0, -1, 0)
    n22 = (0, -1, 0)
    n23 = (0, -1, 0)

    c20 = (1, 0, 1) # Magenta
    c21 = (1, 0, 1)
    c22 = (1, 0, 1)
    c23 = (1, 0, 1)

    uv20 = (0, 0)
    uv21 = (1, 0)
    uv22 = (1, 1)
    uv23 = (0, 1)

    ## Definition des triangles de chaque face 
    # Face avant
    f0 = (0, 1, 2)
    f1 = (0, 2, 3)
    # Face arrière
    f2 = (4, 5, 6)
    f3 = (4, 6, 7)
    # Face droite
    f4 = (8, 9, 10)
    f5 = (8, 10, 11)
    # Face gauche
    f6 = (12, 13, 14)
    f7 = (12, 14, 15)
    # Face supérieure
    f8 = (16, 17, 18)
    f9 = (16, 18, 19)
    # Face inférieure
    f10 = (20, 21, 22)
    f11 = (20, 22, 23)

    # Création des sommets
    sommets = np.array([
        *p0, *n0, *c0, *uv0,
        *p1, *n1, *c1, *uv1,
        *p2, *n2, *c2, *uv2,
        *p3, *n3, *c3, *uv3,
        *p4, *n4, *c4, *uv4,
        *p5, *n5, *c5, *uv5,
        *p6, *n6, *c6, *uv6,
        *p7, *n7, *c7, *uv7,
        *p8, *n8, *c8, *uv8,
        *p9, *n9, *c9, *uv9,
        *p10, *n10, *c10, *uv10,
        *p11, *n11, *c11, *uv11,
        *p12, *n12, *c12, *uv12,
        *p13, *n13, *c13, *uv13,
        *p14, *n14, *c14, *uv14,
        *p15, *n15, *c15, *uv15,
        *p16, *n16, *c16, *uv16,
        *p17, *n17, *c17, *uv17,
        *p18, *n18, *c18, *uv18,
        *p19, *n19, *c19, *uv19,
        *p20, *n20, *c20, *uv20,
        *p21, *n21, *c21, *uv21,
        *p22, *n22, *c22, *uv22,
        *p23, *n23, *c23, *uv23,

    ], dtype=np.float32)

    # Création des indices
    indices = np.array([
        *f0, *f1,
        *f2, *f3,
        *f4, *f5,
        *f6, *f7,
        *f8, *f9,
        *f10, *f11
    ], dtype=np.uint32)

    return sommets, indices





