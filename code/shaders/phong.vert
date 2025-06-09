#version 330 core

layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normale;
layout (location = 2) in vec3 couleur;
layout (location = 3) in vec2 uv;

// Gérer les déplacements
uniform vec4 translation;
uniform mat4 rotation;
uniform mat4 projection;


out vec3 v_color;
out vec3 v_normale;
out vec3 frag_pos;
out vec2 frag_uv;
out vec3 coordonnee_3d;
out vec3 coordonnee_3d_locale;

void main() {
  // Déplacements
  coordonnee_3d = position;
  vec4 p = rotation*vec4(position, 1.0)+translation;
  coordonnee_3d_locale = p.xyz;
  p = projection*p;
  gl_Position = p;

  v_color = couleur;

  v_normale = normale;
  frag_pos = position;
  frag_uv = uv;

}
