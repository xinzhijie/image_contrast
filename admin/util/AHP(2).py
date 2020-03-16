#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import os
import openpyxl


class AHP():
    def __init__(self, up_tri_mat):
        self.row = up_tri_mat.shape[0]

    #Complete the given upper triangular matrix
    def supp_mat(self, up_tri_mat):
        mat = np.eye(self.row)
        for i in range(self.row):
            for j in range(self.row):
                if j > i:
                   mat[i][j] = up_tri_mat[i][j]
                else:
                    mat[i][j] = 1 / up_tri_mat[j][i]

        return mat

    #Get the maximum eigenvalue of the matrix and the corresponding eigenvector
    def get_evec(self, mat):
        eval, evec = np.linalg.eig(mat)
        max_eval = max(list(eval))
        index = list(eval).index(max_eval)
        cor_evec = evec[:, index]
        cor_evec_mod = [abs(a) for a in cor_evec]

        return cor_evec_mod

    #Normalize the vector to the[0, 10] interval
    def normalization_vec(self, vec):
        coe = (10 - 0)/(max(vec) - min(vec))
        nor_vec = [0 + coe*(v - min(vec))for v in vec]
        return ['%.2f' %v for v in nor_vec]

    #Save data to exel file
    def save_result(self, data):
        file_path = os.path.abspath('./result.xlsx')
        if os.path.exists(file_path):         #Judge if the excel file exists
           print('The result file exists in the current path, please check.')
           return
        else:
            wb = openpyxl.Workbook()
            ws1 = wb.active
            ws1['A1'] = 'Data'
            ws1['B1'] = 'Score'
            for row in range(2,len(data)+2):
                ws1[row][0].value = row - 1
                ws1[row][1].value = str(data[row-2])
            wb.save('result.xlsx')
            print('The result is already saved under the path', file_path)


if __name__ == '__main__':
    M = np.array([[1,3,3,5,5,3,5,3,5,5],[0,1,3,5,5,3,5,3,5,5],[0,0,1,3,3,5,5,3,3,5],[0,0,0,1,1,1,3,5,3,5],[0,0,0,0,1,1,3,3,5,5], [0,0,0,0,0,1,3,3,5,5], [0,0,0,0,0,0,1,3,3,5], [0,0,0,0,0,0,0,1,3,5],[0,0,0,0,0,0,0,0,1,3],[0,0,0,0,0 ,0,0,0,0,1]])
    obj = AHP(M)
    # print(obj.supp_mat(M))
    evec = obj.get_evec(obj.supp_mat(M))
    print(obj.normalization_vec(evec))
    # print(evec)

    # obj.save_result(obj.normalization_vec(evec))
#

