
uniform sampler2D u_tex01;

varying vec4 v_normal;
varying vec4 v_s;
varying vec4 v_h;
varying vec2 v_uv;

uniform vec4 u_light_diffuse;
uniform vec4 u_light_specular;

uniform vec4 u_material_diffuse;
uniform vec4 u_material_specular;
uniform float u_material_shininess;

uniform sampler2D texture;

void main(void)
{
    vec4 mat_diffuse = u_material_diffuse * texture2D(u_tex01, v_uv);

    // At this point v_normal and v_s are not normalized so we need to make sure that they are
    float lambert   = max(0.0, dot(v_normal, v_s) / (length(v_normal) * length(v_s)));
    float phong     = max(0.0, dot(v_normal, v_h) / (length(v_normal) * length(v_h)));

    gl_FragColor    = u_light_diffuse * mat_diffuse * lambert
                    + u_light_specular * u_material_specular * pow(phong, u_material_shininess);

}