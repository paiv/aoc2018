// c++ -std=c++11 -shared -fPIC solve.cpp -o build/solve.dylib
#include <vector>

using namespace std;


extern "C"
int solve(int h, int w, char* grid[]) {

    typedef vector<char> state_row;
    typedef vector<state_row> state_t;
    vector<state_t> rounds;

    state_t state;
    for (int y = 0; y < h; y ++) {
        state.emplace_back(&grid[y][0], &grid[y][w]);
    }
    rounds.push_back(state);

    int seen = -1;
    int round = 1;
    for (; ; round++) {
        state_t next_state = state_t(h, state_row(w, '.'));
        for (int y = 0; y < h; y++) {
            for (int x = 0; x < w; x++) {
                char c = state[y][x];
                int te = 0;
                int ya = 0;

                for (int p = max(0, y - 1); p < min(h, y + 2); p++) {
                    for (int q = max(0, x - 1); q < min(w, x + 2); q++) {
                        if ((p != y) || (q != x)) {
                            te += state[p][q] == '|';
                            ya += state[p][q] == '#';
                        }
                    }
                }

                switch (c) {
                    case '.':
                        next_state[y][x] = te > 2 ? '|' : '.';
                        break;
                    case '|':
                        next_state[y][x] = ya > 2 ? '#' : '|';
                        break;
                    case '#':
                        next_state[y][x] = (te && ya) ? '#' : '.';
                        break;
                }
            }
        }

        state = next_state;

        auto it = find(begin(rounds), end(rounds), state);
        if (it != rounds.end()) {
            seen = distance(rounds.begin(), it);
            break;
        }
        rounds.push_back(state);
    }

    state = rounds[seen + (1000000000 - seen) % (round - seen)];

    int te = 0;
    int ya = 0;
    for (int y = 0; y < h; y++) {
        for (int x = 0; x < w; x++) {
            te += state[y][x] == '|';
            ya += state[y][x] == '#';
        }
    }

    return te * ya;
}
