#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import abstractmethod
import numpy as np
import sympy

class GenericCell:
    ""

    def __init__(self, nodes):
        self.nodes = nodes

        self.normal, self._normal = self._normal, self.normal
        self.surface, self._surface = self._surface, self.surface
        self.volume, self._volume = self._volume, self.volume
        self.get_param_coordinate, self._get_param_coordinate = (
            self._get_param_coordinate, self.get_param_coordinate
        )

    def _normal(self):
        return self._normal(np.arange(self.nn)[None,:], self.nodes)

    def _surface(self):
        return self._surface(np.arange(self.nn)[None,:], self.nodes)

    def _volume(self):
        return self._volume(np.arange(self.nn)[None,:], self.nodes)

    def _get_param_coordinate(self, points):
        return self._get_param_coordinate(self.nodes, points)

    @classmethod
    @abstractmethod
    def volume(cls, cells, nodes):
        """
        Returning the volume of each 3D cells.

        Parameters
        ==========
        cells: array_like of size (M, self.nn)
            nodes indexes for each cell
        nodes: array_like of size N, 2|3
            x,y(,z) coordinates

        Returns
        =======
        out: ndarray of size M
            volume of each cells.

        """
        pass

    @classmethod
    @abstractmethod
    def surface(cls, cells, nodes):
        """
        Returning the surface of each 2D cells.

        Parameters
        ==========
        cells: array_like of size (M, self.nn)
            nodes indexes for each cell
        nodes: array_like of size N, 2|3
            x,y(,z) coordinates

        Returns
        =======
        out: ndarray of size M
            surface of each cells.

        """
        pass

    @classmethod
    @abstractmethod
    def normal(cls, cells, nodes):
        """
        Returning the surface normal of each 2D cells.

        Parameters
        ==========
        cells: array_like of size (M, self.nn)
            nodes indexes for each cell
        nodes: array_like of size N, 2|3
            x,y(,z) coordinates

        Returns
        =======
        out: ndarray of size M
            surface normal of each cells.

        """
        pass

    @classmethod
    def is_inside(cls, points):
        """
        Check for each point if it's inside the element

        Parameters
        ==========
        points: array_like of size N, 2|3
            x,y(,z) coordinates

        Returns
        =======
        out: ndarray of size N
            True if inside False if not.

        """
        test = np.ones(len(points), dtype='bool')
        for rule in cls._N:
            test &= (rule(*points.T[:cls.ndim]) >= -cls.EPSILON)
        return test

    @classmethod
    def N(cls, points):
        """
        Compute shape functions at point coordinate

        Parameters
        ==========
        points: array_like of size N, 2|3
            x,y(,z) coordinates

        Returns
        =======
        out: ndarray of shape (P, M)
            shape functions at point coordinate assuming P shape functions

        """
        return np.vstack([N(*points.T[:cls.ndim]) for N in cls._N])

    @classmethod
    def dNdv(cls, v, points):
        """
        Compute component part of Jacobian matrix of shape functions at point coordinate

        Parameters
        ==========
        v: sympy.core.symbol.Symbol
            component used for derivative calculations
        points: array_like of size N, 2|3
            x,y(,z) coordinates

        Returns
        =======
        out: ndarray of shape (P, M)
            component part of Jacobian matrix of shape functions at point coordinate assuming P shape functions

        """
        result = np.zeros((cls.nn, len(points)), dtype='f8')
        for i, dN in enumerate(cls._dN[v]):
            result[i,:] = dN(*points.T)
        return result

    @classmethod
    def dN(cls, points):
        """
        Compute Jacobian matrix of shape functions at point coordinate for all component

        Parameters
        ==========
        points: array_like of size N, 2|3
            x,y(,z) coordinates

        Returns
        =======
        out: generator
            component part of Jacobian matrix of shape functions at point coordinate assuming P shape functions for all component

        """
        return [cls.dNdv(v, points) for v in range(cls.ndim)]

    @classmethod
    def N_data(cls):
        """
        Returns matrix form of shape functions.
        """
        return cls._N_data

    @classmethod
    def dNdv_data(cls, var):
        """
        Returns matrix form of derivative shape functions at `var`.
        """
        return cls._dN_data[var]

    @classmethod
    def dN_data(cls):
        """
        Returns matrix form of derivative shape functions for each parameters.
        """
        return [cls.dNdv_data(v) for v in cls.symbols]

    @classmethod
    def get_gauss_points(cls, weight=True, reduced_integration=False):
        """
        Returns Gauss point(s) of the Cell element

        Parameters
        ==========
        reduced_integration: boolean

        Returns
        =======
        out: tuple
            gauss point(s)
            4 tuple are used to described gauss points:

             * r values
             * s values
             * t values
             * w values

        """
        if weight:
            if reduced_integration:
                return cls.gauss_reduced, cls.gauss_reduced_w
            else:
                return cls.gauss, cls.gauss_w
        else:
            if reduced_integration:
                return cls.gauss_reduced
            else:
                return cls.gauss

    @classmethod
    def get_param_coordinate(cls, nodes, points):
        xx, yy, zz = nodes.T
        xpix, ypix, zpix = points.T

        Np = len(points)

        pg = np.zeros((Np, cls.ndim), dtype='f8')
        wg = np.zeros(Np, dtype='f8')

        res = np.ones(Np, dtype='f8')
        detJ = np.ones(Np, dtype='f8')

        N = np.zeros((cls.nn, Np), dtype='f8')
        dNdr = np.zeros((cls.nn, Np), dtype='f8')
        dNds = np.zeros((cls.nn, Np), dtype='f8')
        if cls.ndim == 3:
            dNdt = np.zeros((cls.nn, Np), dtype='f8')

        dxdr = np.zeros(Np, dtype='f8')
        dydr = np.zeros(Np, dtype='f8')
        dxds = np.zeros(Np, dtype='f8')
        dyds = np.zeros(Np, dtype='f8')
        if cls.ndim == 3:
            dzdr = np.zeros(Np, dtype='f8')
            dzds = np.zeros(Np, dtype='f8')
            dxdt = np.zeros(Np, dtype='f8')
            dydt = np.zeros(Np, dtype='f8')
            dzdt = np.zeros(Np, dtype='f8')

        xp = np.zeros(Np, dtype='f8')
        yp = np.zeros(Np, dtype='f8')
        if cls.ndim == 3:
            zp = np.zeros(Np, dtype='f8')

        idx = np.ones(Np, dtype='bool')

        for niter in range(1000):

            if cls.ndim == 2:
                N[:,idx] = cls.N(pg[idx])
                dNdr[:,idx], dNds[:,idx] = cls.dN(pg[idx])
            else:
                N[:,idx] = cls.N(pg[idx])
                dNdr[:,idx], dNds[:,idx], dNdt[:,idx] = cls.dN(pg[idx])

            dxdr[idx] = dNdr[:,idx].T.dot(xx)
            dydr[idx] = dNdr[:,idx].T.dot(yy)
            dxds[idx] = dNds[:,idx].T.dot(xx)
            dyds[idx] = dNds[:,idx].T.dot(yy)

            if cls.ndim == 2:
                detJ[idx] = dxdr[idx]*dyds[idx] - dydr[idx]*dxds[idx]
            else:
                dxdt[idx] = dNdt[:,idx].T.dot(xx)
                dydt[idx] = dNdt[:,idx].T.dot(yy)
                dzdr[idx] = dNdr[:,idx].T.dot(zz)
                dzds[idx] = dNds[:,idx].T.dot(zz)
                dzdt[idx] = dNdt[:,idx].T.dot(zz)
                detJ[idx] = (dxdr[idx]*dyds[idx]*dzdt[idx] +
                            dxdt[idx]*dydr[idx]*dzds[idx] +
                            dxds[idx]*dydt[idx]*dzdr[idx] -
                            dxdt[idx]*dyds[idx]*dzdr[idx] -
                            dxdr[idx]*dydt[idx]*dzds[idx] -
                            dxds[idx]*dydr[idx]*dzdt[idx])

            wg[idx & (detJ <= 0)] = np.nan

            idx[:] = (res > 1.e-12) & (detJ > 0)

            if not idx.any():
                break

            if cls.ndim == 2:
                invJ = np.vstack((
                    dyds[idx]/detJ[idx],
                    -dxds[idx]/detJ[idx],
                    -dydr[idx]/detJ[idx],
                    dxdr[idx]/detJ[idx]
                ))
            else:
                invJ = np.vstack((
                    (dyds[idx]*dzdt[idx] - dydt[idx]*dzds[idx]) / detJ[idx],
                    -(dxds[idx]*dzdt[idx] - dxdt[idx]*dzds[idx]) / detJ[idx],
                    (dxds[idx]*dydt[idx] - dxdt[idx]*dyds[idx]) / detJ[idx],
                    -(dydr[idx]*dzdt[idx] - dydt[idx]*dzdr[idx]) / detJ[idx],
                    (dxdr[idx]*dzdt[idx] - dxdt[idx]*dzdr[idx]) / detJ[idx],
                    -(dxdr[idx]*dydt[idx] - dxdt[idx]*dydr[idx]) / detJ[idx],
                    (dydr[idx]*dzds[idx] - dyds[idx]*dzdr[idx]) / detJ[idx],
                    -(dxdr[idx]*dzds[idx] - dxds[idx]*dzdr[idx]) / detJ[idx],
                    (dxdr[idx]*dyds[idx] - dxds[idx]*dydr[idx]) / detJ[idx],
                ))

            xp[idx] = N[:,idx].T.dot(xx)
            yp[idx] = N[:,idx].T.dot(yy)
            if cls.ndim == 3:
                zp[idx] = N[:,idx].T.dot(zz)

            if cls.ndim == 2:
                dxg = invJ[0,:]*(xpix[idx]-xp[idx])+invJ[1,:]*(ypix[idx]-yp[idx])
                dyg = invJ[2,:]*(xpix[idx]-xp[idx])+invJ[3,:]*(ypix[idx]-yp[idx])
                dzg = 0
            else:
                dxg = invJ[0,:]*(xpix[idx]-xp[idx])+invJ[1,:]*(ypix[idx]-yp[idx])+invJ[2,:]*(zpix[idx]-zp[idx])
                dyg = invJ[3,:]*(xpix[idx]-xp[idx])+invJ[4,:]*(ypix[idx]-yp[idx])+invJ[5,:]*(zpix[idx]-zp[idx])
                dzg = invJ[6,:]*(xpix[idx]-xp[idx])+invJ[7,:]*(ypix[idx]-yp[idx])+invJ[8,:]*(zpix[idx]-zp[idx])

            res[idx] = dxg*dxg + dyg*dyg + dzg*dzg

            pg[idx,0] += dxg
            pg[idx,1] += dyg
            if cls.ndim == 3:
                pg[idx,2] += dzg

            idx[:] = (res > 1.e-12) & (detJ > 0)

            if not idx.any():
                break

        idx = ~np.isnan(wg)

        if cls.ndim == 2:
            idx[idx] &= cls.is_inside(pg[idx])
        else:
            idx[idx] &= cls.is_inside(pg[idx])
        wg[idx] = 1
        wg[~idx] = 0
        pg[~idx] = 0

        if cls.ndim == 2:
            pg = np.hstack((pg, pg[:,[0]]*0))

        return pg, wg


class Cell(type):
    """
    Cell(name, vtk_id, ndim, order, shapes, gauss_reduced, gauss, surface=None, volume=None, normal=None, vertices=[], faces=[])

    A Cell object is a definition of a mesh element in term or FEM element.

    Parameters
    ==========
    name: string
        name of the cell type
    vtk_id: integer
        see [VTK File Format]
    ndim : integer
        2 for 2D, 3 for 3D
    order: integer
        1 for linear, 2 for quadratic
    shapes : tuple
        shapes function of the FEM element
        each shape is described by a sympy function of r, s and t (if 3D)
    gauss_reduced : tuple
        gauss point for reduced integration
        4 tuple are used to described gauss points:

         * r values
         * s values
         * t values
         * w values
    gauss : tuple
        gauss points for the first order
        4 tuple are used to described gauss points:

         * r values
         * s values
         * t values
         * w values
    surface : function
        function f(cells, xn, yn) returning the surface of each 2D cells
    normal : function
        function f(cells, xn, yn) returning the normal of each 2D cells
    volume : function
        function f(cells, xn, yn, zn) returning the volume of each 3D cells
    vertices : tuple
        couples of nodes indices for each vertices of the cell
    faces : tuple
        triplet of nodes indices for each triangle face of 3D cell
        quadruplet of nodes indices for each quadrangle face of 3D cell

    """
    _by_vtk_id = {}
    _by_name = {}
    _list = []
    EPSILON = 0

    def __new__(cls, name, bases, classdict):
        result = type.__new__(cls, name, bases, classdict)
        symbols = set()
        if result.order > 0:
            for x in result.shapes:
                symbols = symbols.union(x.as_poly().free_symbols)
        result.symbols = list(symbols)
        result.symbols.sort(key=str)
        result._N = [sympy.lambdify(result.symbols, shape) for shape in result.shapes]
        result._dN = [[sympy.lambdify(result.symbols, shape.diff(symbol)) for shape in result.shapes] for symbol in result.symbols]

        result._N_data = (
            np.tile(np.mgrid[[slice(0,2) for _ in range(len(result.symbols))]].reshape(len(result.symbols), 2**len(result.symbols)).T, (len(result.shapes), 1, 1)),
            np.zeros((len(result.shapes), 2**len(result.symbols)))
        )

        if len(result.symbols) > 0:

            for i, shape in enumerate(result.shapes):
                poly = shape.as_poly(result.symbols)
                mask = list(map(result.symbols.index, poly.args[1:]))
                for idx, c in poly.terms():
                    B = np.zeros(len(result.symbols), dtype=int)
                    B[mask] = idx
                    result._N_data[1][i,np.where((result._N_data[0][0] == B).all(axis=1))[0]] = c

        result._dN_data = {}

        for var in result.symbols:
            result._dN_data[var] = (
                np.tile(np.mgrid[[slice(0,2) for _ in range(len(result.symbols))]].reshape(len(result.symbols), 2**len(result.symbols)).T, (len(result.shapes), 1, 1)),
                np.zeros((len(result.shapes), 2**len(result.symbols)))
            )

            for i, shape in enumerate(result.shapes):
                poly = shape.as_poly(result.symbols).diff(var)
                mask = list(map(result.symbols.index, poly.args[1:]))
                for idx, c in poly.terms():
                    B = np.zeros(len(result.symbols), dtype=int)
                    B[mask] = idx
                    result._dN_data[var][1][i,np.where((result._dN_data[var][0][0] == B).all(axis=1))[0]] = c

        if result.ndim > 0:
            result.vertices = np.array(result.vertices)
        result.nn = len(result.shapes)
        gauss_reduced = np.array(result.gauss_reduced)
        result.gauss_reduced = gauss_reduced[:,:-1]
        result.gauss_reduced_w = gauss_reduced[:,-1]
        gauss = np.array(result.gauss)
        result.gauss = gauss[:,:-1]
        result.gauss_w = gauss[:,-1]
        result.ng = len(result.gauss)
        result.name = result.__name__
        cls._by_vtk_id[result.vtk_id] = result
        cls._by_name[result.__name__] = result
        cls._list.append(result)
        return result

    @classmethod
    def by_name(cls, name):
        return cls._by_name[name]

    @classmethod
    def by_vtk_id(cls, vtk_id):
        return cls._by_vtk_id[vtk_id]

    @classmethod
    def iter_by_celltype(cls, cell_dict):
        for T in cls._list:
            if T in cell_dict:
                yield T, cell_dict[T]


r = sympy.var('r')
s = sympy.var('s')
t = sympy.var('t')

class T3(GenericCell, metaclass=Cell):
    ""

    vtk_id = 5
    ndim = 2
    order = 1

    shapes = (
        1-r-s,
        r,
        s,
    )

    gauss_reduced = (
        (1/3, 1/3, 1/2),
    )

    gauss = (
        (1/6, 1/6, 1/6),
        (2/3, 1/6, 1/6),
        (1/6, 2/3, 1/6),
    )

    vertices = (
        (0, 1),
        (1, 2),
        (2, 0),
    )

    @classmethod
    def normal(cls, cells, nodes):
        a_b = (nodes[cells[:,1]] - nodes[cells[:,0]]).T
        a_c = (nodes[cells[:,2]] - nodes[cells[:,0]]).T

        return -np.vstack((a_c[1,:]*a_b[2,:] - a_c[2,:]*a_b[1,:],
                           a_c[2,:]*a_b[0,:] - a_c[0,:]*a_b[2,:],
                           a_c[0,:]*a_b[1,:] - a_c[1,:]*a_b[0,:]))

    @classmethod
    def surface(cls, cells, nodes):
        n = cls.normal(cells, nodes)
        return 1/2*(n[0,:]**2+n[1,:]**2+n[2,:]**2)**.5


class Q4(GenericCell, metaclass=Cell):
    ""

    vtk_id = 9
    ndim = 2
    order = 1

    shapes = (
        0.25*(1-r)*(1-s),
        0.25*(1+r)*(1-s),
        0.25*(1+r)*(1+s),
        0.25*(1-r)*(1+s),
    )

    gauss_reduced = (
        (0., 0., 4.),
    )

    gauss = (
        (-1/3**.5, -1/3**.5, 1.),
        ( 1/3**.5, -1/3**.5, 1.),
        ( 1/3**.5,  1/3**.5, 1.),
        (-1/3**.5,  1/3**.5, 1.),
    )

    vertices = (
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),
    )

    @classmethod
    def normal(cls, cells, nodes):
        return T3.normal(cells[:,[0,1,2]], nodes) + T3.normal(cells[:,[2,3,0]], nodes)

    @classmethod
    def surface(cls, cells, nodes):
        n = cls.normal(cells, nodes)
        return 1/2*(n[0,:]**2+n[1,:]**2+n[2,:]**2)**.5


class T4(GenericCell, metaclass=Cell):
    ""

    vtk_id = 10
    ndim = 3
    order = 1

    shapes = (
        s,
        t,
        1-r-s-t,
        r,
    )

    gauss_reduced = (
        (1/4, 1/4, 1/4, 1/6),
    )

    gauss = (
        ((5 - 5**.5)/20, (5 - 5**.5)/20, (5 - 5**.5)/20, 1/24),
        ((5 - 5**.5)/20, (5 - 5**.5)/20, (5+3*5**.5)/20, 1/24),
        ((5 - 5**.5)/20, (5+3*5**.5)/20, (5 - 5**.5)/20, 1/24),
        ((5+3*5**.5)/20, (5 - 5**.5)/20, (5 - 5**.5)/20, 1/24),
    )

    vertices = (
        (0, 1),
        (1, 2),
        (2, 0),
        (0, 3),
        (1, 3),
        (2, 3),
    )

    faces = (
        (0, 2, 1),
        (0, 3, 2),
        (2, 3, 1),
        (0, 1, 3),
    )

    @classmethod
    def volume(cls, cells, nodes):
        a_d = (nodes[cells[:,0]] - nodes[cells[:,3]]).T
        b_d = (nodes[cells[:,1]] - nodes[cells[:,3]]).T
        c_d = (nodes[cells[:,2]] - nodes[cells[:,3]]).T

        b_dxc_d = np.vstack((b_d[1,:]*c_d[2,:]-b_d[2,:]*c_d[1,:],
                            b_d[2,:]*c_d[0,:]-b_d[0,:]*c_d[2,:],
                            b_d[0,:]*c_d[1,:]-b_d[1,:]*c_d[0,:]))

        return 1/6*abs(a_d[0,:]*b_dxc_d[0,:]+a_d[1,:]*b_dxc_d[1,:]+a_d[2,:]*b_dxc_d[2,:])


class C8(GenericCell, metaclass=Cell):
    ""

    vtk_id = 12
    ndim = 3
    order = 1

    shapes = (
        0.125*(1-r)*(1-s)*(1-t),
        0.125*(1+r)*(1-s)*(1-t),
        0.125*(1+r)*(1+s)*(1-t),
        0.125*(1-r)*(1+s)*(1-t),
        0.125*(1-r)*(1-s)*(1+t),
        0.125*(1+r)*(1-s)*(1+t),
        0.125*(1+r)*(1+s)*(1+t),
        0.125*(1-r)*(1+s)*(1+t),
    )

    gauss_reduced = (
        (0., 0., 0., 8.,),
    )

    gauss = (
        (-1/3**.5, -1/3**.5, -1/3**.5, 1.),
        (-1/3**.5, -1/3**.5,  1/3**.5, 1.),
        (-1/3**.5,  1/3**.5, -1/3**.5, 1.),
        (-1/3**.5,  1/3**.5,  1/3**.5, 1.),
        ( 1/3**.5, -1/3**.5, -1/3**.5, 1.),
        ( 1/3**.5, -1/3**.5,  1/3**.5, 1.),
        ( 1/3**.5,  1/3**.5, -1/3**.5, 1.),
        ( 1/3**.5,  1/3**.5,  1/3**.5, 1.),
    )

    vertices = (
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 4),
        (0, 4),
        (1, 5),
        (2, 6),
        (3, 7),
    )

    faces = (
        (0, 3, 2, 1),
        (0, 1, 5, 4),
        (0, 4, 7, 3),
        (3, 7, 6, 2),
        (4, 5, 6, 7),
        (2, 6, 5, 1),
    )

    @classmethod
    def volume(cls, cells, nodes):
        pd = nodes[cells].mean(axis=1)

        vol = 0
        for i, j, k in [
            (0, 1, 2),
            (2, 3, 0),
            (4, 5, 6),
            (6, 7, 4),
            (3, 2, 7),
            (7, 6, 2),
            (2, 1, 5),
            (5, 6, 2),
            (1, 5, 4),
            (4, 0, 1),
            (0, 4, 7),
            (7, 3, 0)]:

            a_d = (nodes[cells[:,i]] - pd).T
            b_d = (nodes[cells[:,j]] - pd).T
            c_d = (nodes[cells[:,k]] - pd).T

            b_dxc_d = np.vstack((b_d[1,:]*c_d[2,:]-b_d[2,:]*c_d[1,:],
                                 b_d[2,:]*c_d[0,:]-b_d[0,:]*c_d[2,:],
                                 b_d[0,:]*c_d[1,:]-b_d[1,:]*c_d[0,:]))

            vol += 1/6*abs(a_d[0,:]*b_dxc_d[0,:]+a_d[1,:]*b_dxc_d[1,:]+a_d[2,:]*b_dxc_d[2,:])

        return vol


class P6(GenericCell, metaclass=Cell):
    ""

    vtk_id = 13
    ndim = 3
    order = 1

    shapes = (
        0.5*s*(1-r),
        0.5*t*(1-r),
        0.5*(1-s-t)*(1-r),
        0.5*s*(1+r),
        0.5*t*(1+r),
        0.5*(1-s-t)*(1+r),
    )

    gauss_reduced = (
        (0., 1/3, 1/3, 1.,),
    )

    gauss = (
        (-1/3**.5, 0.5, 0.5, 1/6),
        (-1/3**.5, 0.0, 0.5, 1/6),
        (-1/3**.5, 0.5, 0.0, 1/6),
        ( 1/3**.5, 0.5, 0.5, 1/6),
        ( 1/3**.5, 0.0, 0.5, 1/6),
        ( 1/3**.5, 0.5, 0.0, 1/6),
    )

    vertices = (
        (0, 1),
        (1, 2),
        (2, 0),
        (3, 4),
        (4, 5),
        (5, 4),
        (0, 3),
        (2, 5),
        (1, 4),
    )

    faces = (
        (0, 2, 1),
        (3, 4, 5),
        (0, 3, 5, 2),
        (2, 5, 4, 1),
        (1, 4, 3, 0),
    )

    @classmethod
    def volume(cls, cells, nodes):
        pd = nodes[cells].mean(axis=1)

        vol = 0

        for i, j, k in [
            (0, 1, 2),
            (0, 2, 5),
            (5, 3, 0),
            (0, 3, 4),
            (4, 1, 0),
            (1, 4, 5),
            (5, 2, 1),
            (3, 4, 5)]:

            a_d = (nodes[cells[:,i]] - pd).T
            b_d = (nodes[cells[:,j]] - pd).T
            c_d = (nodes[cells[:,k]] - pd).T

            b_dxc_d = np.vstack((b_d[1,:]*c_d[2,:]-b_d[2,:]*c_d[1,:],
                                b_d[2,:]*c_d[0,:]-b_d[0,:]*c_d[2,:],
                                b_d[0,:]*c_d[1,:]-b_d[1,:]*c_d[0,:]))

            vol += 1/6*abs(a_d[0,:]*b_dxc_d[0,:]+a_d[1,:]*b_dxc_d[1,:]+a_d[2,:]*b_dxc_d[2,:])

        return vol


class T4Q(GenericCell, metaclass=Cell):
    ""

    vtk_id = 24
    ndim = 3
    order = 2

    shapes = (
        s*(2*s-1),
        t*(2*t-1),
        (1-r-s-t)*(1-2*r-2*s-2*t),
        r*(2*r-1),
        4*s*t,
        4*t*(1-r-s-t),
        4*s*(1-r-s-t),
        4*r*s,
        4*r*t,
        4*r*(1-r-s-t)
    )

    gauss_reduced = T4.gauss_reduced

    gauss = T4.gauss

    vertices = T4.vertices

    faces = T4.faces

    @classmethod
    def volume(cls, cells, nodes):
        return T4.volume(cells, nodes)


class T3Q(GenericCell, metaclass=Cell):
    ""

    vtk_id = 22
    ndim = 2
    order = 2

    shapes = (
        -(1-r-s)*(1-2*(1-r-s)),
        -r*(1-2*r),
        -s*(1-2*s),
        4*r*(1-r-s),
        4*r*s,
        4*s*(1-r-s)
    )

    gauss_reduced = T3.gauss_reduced

    gauss = T3.gauss

    vertices = T3.vertices

    @classmethod
    def normal(cls, cells, nodes):
        return T3.normal(cells, nodes)

    @classmethod
    def surface(cls, cells, nodes):
        return T3.surface(cells, nodes)


class P1(GenericCell, metaclass=Cell):
    ""

    vtk_id = 1
    ndim = 0
    order = 0

    shapes = (sympy.core.numbers.One(),)

    gauss_reduced = (
        (0,),
    )

    gauss = (
        (0,),
    )


class S2(GenericCell, metaclass=Cell):
    ""

    vtk_id = 3
    ndim = 1
    order = 1

    shapes = (
        0.5*(1-r),
        0.5*(1+r)
    )

    gauss_reduced = (
        (0, 2,),
    )

    gauss = (
        ( 0.577350269189626, 1.0),
        (-0.577350269189626, 1.0),
    )

    vertices = (
        (0, 1),
    )
