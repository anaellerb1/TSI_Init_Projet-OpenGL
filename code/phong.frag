#version 330 core

// Variable de sortie (sera utilisé comme couleur)
out vec4 color;

in vec3 coordonnee_3d;
in vec3 coordonnee_3d_locale;
in vec3 vnormale;
in vec3 v_color;
in vec2 frag_uv;

uniform sampler2D texture0;
vec3 light = vec3(0.5,0.5,5.0);


//Un Fragment Shader minimaliste
void main (void)
{
  vec3 n = normalize(vnormale);
  vec3 d = normalize(light-coordonnee_3d_locale);
  vec3 r = reflect(-d,n);
  vec3 o = normalize(-coordonnee_3d_locale);

  float diffuse  = 0.7*clamp(dot(n,d),0.0,1.0);
  
  // fait des reflets 
  //float specular = 0.2*pow(clamp(dot(r,o),0.0,1.0),128.0);
  float specular = 1.0*pow(clamp(dot(r,o), 0.0, 1.0), 32.0);

  float ambiant  = 0.2;


  vec4 white = vec4(1.0,1.0,1.0,0.0);

  vec4 color_texture = texture(texture0, frag_uv);
  vec4 color_final = color_texture;

  color = (ambiant + diffuse) * color_texture + specular * vec4(1.0);


}
