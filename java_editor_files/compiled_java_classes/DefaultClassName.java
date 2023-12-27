#include <iostream>
#include <map>
#include <random>
#include <bits/stdc++.h>

double calculate_percentage(const std::map<std::string, double>& subjects) {
    double total_marks = 0;
    double total_subjects = subjects.size();

    for (const auto& subject : subjects) {
        total_marks += subject.second;
    }

    double percentage = (total_marks / (total_subjects * 100)) * 100;
    return percentage;
}

int main() {
    // Generate a random number of subjects (between 1 and 10)
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<int> subjects_distribution(1, 10);
    int num_subjects = subjects_distribution(gen);

    std::map<std::string, double> subjects;

    for (int i = 0; i < num_subjects; ++i) {
        std::string subject_name = "Subject_" + std::to_string(i + 1);
        // Generate random marks (between 0 and 100)
        std::uniform_real_distribution<double> marks_distribution(0.0, 100.0);
        double marks = marks_distribution(gen);
        subjects[subject_name] = marks;
    }

    double percentage = calculate_percentage(subjects);

    std::cout << "\nSubject-wise marks:" << std::endl;
    for (const auto& subject : subjects) {
        std::cout << subject.first << ": " << subject.second << std::endl;
    }

    std::cout << "\nPercentage: " << std::fixed << std::setprecision(2) << percentage << "%" << std::endl;

    return 0;
}
