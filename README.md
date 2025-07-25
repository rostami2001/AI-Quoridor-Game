# AI Quoridor Game Solver with Minimax and Alpha-Beta Pruning

An implementation of the strategic board game **Quoridor** with an AI opponent using adversarial search algorithms (Minimax + Alpha-Beta pruning). Developed as part of the *Artificial Intelligence* course (2024).

---

## Features
- **Game Rules**:  
  - Two-player game on a 7×7 board where players race to reach the opposite side.  
  - Players can **move** (up/down/left/right) or **place walls** to block opponents.  
  - Custom rule: Walls can only be placed within 2 blocks of the opponent (optimization for faster gameplay).  

- **AI Components**:  
  - **Minimax Algorithm** with configurable depth.  
  - **Alpha-Beta Pruning** for optimized performance.  
  - **Heuristic Function**: Evaluates board state based on shortest path to goal and opponent blocking.  

- **Visualization**:  
  - ASCII-based board display with walls (`|`, `—`) and player tokens (`1`, `2`).  
