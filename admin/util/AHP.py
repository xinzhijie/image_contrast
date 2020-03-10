#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import os
import openpyxl
import xlrd


class AHP():
    def __init__(self, up_tri_mat):
        self.row = up_tri_mat.shape[0]

    #Complete the given upper triangular matrix
    def supp_mat(self, up_tri_mat):
        mat = np.eye(self.row)
        for i in range(self.row):
            for j in range(self.row):
                if j > i:
                   mat[i][j] = 1 / up_tri_mat[i][j]
                else:
                    mat[i][j] = up_tri_mat[j][i]

        return mat

    #Get the maximum eigenvalue of the matrix and the corresponding eigenvector
    def get_evec(self, mat):
        eval, evec = np.linalg.eig(mat)
        max_eval = max(list(eval))
        index = list(eval).index(max_eval)
        cor_evec = evec[:, index]
        cor_evec_mod = [abs(a) for a in cor_evec]

        return cor_evec_mod

    #Save data to exel file
    def save_result(self, data, folder):
        file_path = os.path.abspath(folder + '\\result.xlsx')
        if os.path.exists(file_path):         #Judge if the excel file exists
            os.remove(file_path)
            print('The result file exists in the current path, please check.')
        wb = openpyxl.Workbook()
        ws1 = wb.active
        ws1['A1'] = 'Data'
        ws1['B1'] = 'Score'
        for row in range(2,len(data)+2):
            ws1[row][0].value = row - 1
            ws1[row][1].value = str(data[row-2])
        wb.save(folder + '//result.xlsx')
        print('The result is already saved under the path', file_path)


if __name__ == '__main__':

    filename = "data.xlsx"
    arr = []
    ex = xlrd.open_workbook(filename).sheets()[0]
    for i in range(ex.nrows):
        print(i)
        col = ex.row_values(i)
        for index, n in enumerate(col):
            if isinstance(n, str):
                col[index] = 0
        arr.append(col)
    M = np.array(arr)
    obj = AHP(M)
    evec = obj.get_evec(obj.supp_mat(M))
    obj.save_result(evec)


