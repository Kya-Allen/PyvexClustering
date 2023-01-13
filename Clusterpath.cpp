#include <iostream>
#include <vector>

//default to each observation/subject being an individual subvector nested within the supervector

float max_penalty(std::vector<std::vector<float>> data_matrix) {
    // uses a formula to find the max() penalty parameter across each single dimension j
    // then finds the max() penalty across the stored values for for each dimension

    for (int dimension: data_matrix[0]) {
        
        float preliminary_maximums [data_matrix[0].size()] = {};

        float mean = 0;
        for (int i; i <= data_matrix.size(); i++) {
            mean += data_matrix[i][0];
        }
        mean = mean / data_matrix.size();

        float submeans[data_matrix.size()] = {};
        for (int j; j < data_matrix.size(); j++) {
            float submean = 0;
            for (int k; k <= j; k++) {
                submean += data_matrix[k][0];
            }
            submean = submean / j;
            submeans[j] = submean;
        }

        float solutions[data_matrix.size()];

        for (int k: submeans) {
            float term_2 = data_matrix.size() - k;
            float term_1 = mean - submeans[k];
            solutions[k] = term_1 / term_2;

        }

        preliminary_maximums[dimension] = *std::max_element(solutions, solutions + solutions.size());
    }

    return *std::max_element(preliminary_maximums, preliminary_maximums + preliminary_maximums.size());
}

void C_PAINT(std::vector<std::vector<float>> data_matrix, int path_length) { 
    // A dynamic programming algorithm that splits the problem into each of it's dimensions, and solves them sequentially
    // path_length gives the number of different penalty parameter values, to explicate the path structure as the penalty parameter goes from max -> 0

    float penalty = max_penalty(data_matrix) * (1 / path_length);

    float sort_array[data_matrix.size()] = {};
    float sorted_matrix[data_matrix.size][data_matrix[0].size()] = {};
    for (int dimension: data_matrix[0]) {
        sort_array[] 
    }



}

int main() {

    int zorted_matrix[5] = {1, 3, 5, 8, 9};

    std::cout << zorted_matrix[1];
}