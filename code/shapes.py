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
    """
    sommets = np.array([
        *p0, *n0, *c0, *uv0,
        *p1, *n1, *c1, *uv1,
        *p2, *n2, *c2, *uv2,
        *p3, *n3, *c3, *uv3
    ], dtype=np.float32)

    """
    sommets = np.array([
        *p0, *c0,
        *p1, *c1,
        *p2, *c2,
        *p3, *c3
    ], dtype=np.float32)

    # Faces du plan
    f0 = (0, 1, 2) # Triangle inférieur droit
    f1 = (0, 2, 3) # Triangle supérieur gauche

    # Indices 
    indices = np.array([*f0, *f1], dtype=np.uint32)


    return sommets, indices
