#version 330 core

// Variable de sortie (sera utilisé comme couleur)
uniform vec3 uColor;
in vec3 coordonnee_3d;
out vec4 color;


//Un Fragment Shader minimaliste
void main (void)
{
  float r = gl_FragCoord.x/800.0;
  float g = gl_FragCoord.y/800.0;

  color = vec4(coordonnee_3d, 1.0);
}


