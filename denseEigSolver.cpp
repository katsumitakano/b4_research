#include <Eigen/Dense>
#include <iostream>		// 標準入出力ストリーム
#include <fstream>		// ファイル入出力
#include <string>		// 文字列操作
#include <cstdio>		// 標準入出力
#include <ctime>		// 時間計測
#define print(X) cout << X << endl
#define err_print(X) cerr << X << endl

using namespace Eigen;
using namespace std;

/*
 忘れるのでメモ
 col：列
 row：行
*/

MatrixXd loadMatrix(char filename[]){
  int row;
  int col;
  string input;

  ifstream ifs(filename);
  ifs >> input; // 行数を読み出し格納
  row = atoi(input.c_str());
  ifs >> input; // 列数を読み出し格納
  col = atoi(input.c_str());

  // 行列ファイルの読み込み
  MatrixXd matrix(row, col);
  for(int i=0; i<row; i++){
      for(int j=0; j<col; j++){
          ifs >> input;
          matrix(i,j) = atof(input.c_str());
      }
  }
  return matrix;
}

int main(int argc, char* argv[]){
  if(argc <= 1){
    err_print("Usage: ./denseEigSolver matrix.dat");
    return -1;
  }

  MatrixXd Matrix;
  MatrixXd EigVal, EigVec;
  char* matfile;
  char  out_eval[50], out_evec[50];
  clock_t start, end;

  // 行列の読み込み
  matfile = argv[1];
  err_print("Start Loading Matrix."); start = clock();
  Matrix = loadMatrix(matfile);
  err_print("End Loading Matrix."); end = clock();
  cout << "読み込み：" << (double)(end-start)/CLOCKS_PER_SEC << "(s)" << endl;
  
  // 固有値分解実行
  err_print("Start Eigen Solver."); start = clock();
  SelfAdjointEigenSolver<MatrixXd> eig(Matrix);
  err_print("End Eigen Solver."); end = clock();
  cout << "固有値分解：" << (double)(end-start)/CLOCKS_PER_SEC << "(s)" << endl;
  
  // 固有値・固有ベクトルの取得
  EigVal = eig.eigenvalues();
  EigVec = eig.eigenvectors();

  // 保存用のファイル名作成
  sprintf(out_eval, "%s.eval", matfile);
  sprintf(out_evec, "%s.evec", matfile);

  // 固有値・固有ベクトルの書き出し
  ofstream eval(out_eval);
  eval << EigVal << endl;
  ofstream evec(out_evec);
  evec << EigVec << endl;

  return 0;
}
