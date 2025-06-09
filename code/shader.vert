#version 330 core


// Variable d'entrée, ici la position
layout (location = 0) in vec3 position;
layout(location = 1) in vec3 normale; //phong
out vec3 coordonnee_3d;
out vec3 v_normale;


uniform mat4 rotation;
uniform vec4 translation;
uniform mat4 rotation;
uniform mat4 projection;


void main (void)
{
  coordonnee_3d = position;
  v_normale = vec3(0.0, 0.0, 1.0); // temporairement


  //Coordonnees du sommet
  gl_Position = projection * (rotation * vec4(position, 1.0) + translation);

}
