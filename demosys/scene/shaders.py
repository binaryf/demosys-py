import moderngl
import os

from pyrr import Matrix33

from demosys import context
from demosys.conf import settings
from demosys.resources import shaders

settings.add_shader_dir(os.path.join(os.path.dirname(__file__), 'shaders'))


class MeshShader:

    def __init__(self, shader=None, **kwargs):
        self.shader = shader
        self.ctx = context.ctx()

    def draw(self, mesh, proj_mat, view_mat, time=0):
        """
        Draw code for the mesh. Should be overriden.

        :param mesh: The Mesh object to draw
        :param proj_mat: projection matrix (ndarray)
        :param view_mat: View matrix (ndarray)
        :param time: The current time
        """
        self.shader.uniform("m_proj", proj_mat.astype('f4').tobytes())
        self.shader.uniform("m_mv", view_mat.astype('f4').tobytes())
        mesh.vao.draw(self.shader)

    def apply(self, mesh):
        """
        Determine if this MeshShader should be applied to the mesh
        Can return self or some MeshShader instance to support dynamic MeshShader creation

        :param mesh: The mesh to inspect
        """
        raise NotImplementedError("apply is not implemented. Please override the MeshShader method")

    def create_normal_matrix(self, modelview):
        """
        Convert to mat3 and return inverse transpose.
        These are normally needed when dealing with normals in shaders.

        :param modelview: The modelview matrix
        :return: Normal matrix
        """
        normal_m = Matrix33.from_matrix44(modelview)
        normal_m = normal_m.inverse
        normal_m = normal_m.transpose()
        return normal_m


class ColorShader(MeshShader):
    """
    Simple color shader
    """
    def __init__(self, shader=None, **kwargs):
        super().__init__(shader=shaders.get("scene_default/color.glsl", create=True))

    def draw(self, mesh, proj_mat, view_mat, time=0):
        m_normal = self.create_normal_matrix(view_mat)

        if mesh.material:
            if mesh.material.double_sided:
                self.ctx.disable(moderngl.CULL_FACE)
            else:
                self.ctx.enable(moderngl.CULL_FACE)

            if mesh.material.color:
                self.shader.uniform("color", tuple(mesh.material.color))
            else:
                self.shader.uniform("color", (1.0, 1.0, 1.0, 1.0))

        self.shader.uniform("m_proj", proj_mat.astype('f4').tobytes())
        self.shader.uniform("m_mv", view_mat.astype('f4').tobytes())
        self.shader.uniform("m_normal", m_normal.astype('f4').tobytes())

        mesh.vao.draw(self.shader)

    def apply(self, mesh):
        if not mesh.material:
            return None

        if not mesh.attributes.get("NORMAL"):
            return None

        if mesh.material.mat_texture is None:
            return self

        return None


class TextureShader(MeshShader):
    """
    Simple texture shader
    """
    def __init__(self, shader=None, **kwargs):
        super().__init__(shader=shaders.get("scene_default/texture.glsl", create=True))

    def draw(self, mesh, proj_mat, view_mat, time=0):
        m_normal = self.create_normal_matrix(view_mat)

        if mesh.material.double_sided:
            self.ctx.disable(moderngl.CULL_FACE)
        else:
            self.ctx.enable(moderngl.CULL_FACE)

        mesh.material.mat_texture.texture.use()
        self.shader.uniform("texture0", 0)

        self.shader.uniform("m_proj", proj_mat.astype('f4').tobytes())
        self.shader.uniform("m_mv", view_mat.astype('f4').tobytes())
        self.shader.uniform("m_normal", m_normal.astype('f4').tobytes())

        mesh.vao.draw(self.shader)

    def apply(self, mesh):
        if not mesh.material:
            return None

        if not mesh.attributes.get("NORMAL"):
            return None

        if mesh.material.mat_texture is not None:
            return self

        return None


class FallbackShader(MeshShader):
    """
    Fallback shader only rendering positions in white
    """
    def __init__(self, shader=None, **kwargs):
        super().__init__(shader=shaders.get("scene_default/fallback.glsl", create=True))

    def draw(self, mesh, proj_mat, view_mat, time=0):

        self.shader.uniform("m_proj", proj_mat.astype('f4').tobytes())
        self.shader.uniform("m_mv", view_mat.astype('f4').tobytes())

        if mesh.material:
            self.shader.uniform("color", tuple(mesh.material.color[0:3]))
        else:
            self.shader.uniform("color", (1.0, 1.0, 1.0))

        mesh.vao.draw(self.shader)

    def apply(self, mesh):
        return self
