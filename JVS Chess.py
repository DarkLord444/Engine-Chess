#Product of Đạt Nguyễn Tất
#Copyright 2024, DatJVC

#Hello, I am the developer of the JVS Chess Engine.
#Granola JVS Chess Analyzer is a powerful tool designed 
#to support chess players at all levels. Developed by a 
#skilled programmer, Granola JVS integrates advanced algorithms 
#to deliver accurate and optimal move analysis. 
#With a user-friendly interface and smart suggestion capabilities, 
#Granola JVS helps players refine their tactical skills, capitalize 
#on opportunities, and avoid common mistakes. Moreover, 
#this analyzer is optimized for effective performance across 
#multiple platforms, providing a seamless and fast experience 
#for users.

import chess
import pickle

class ImprovedChessEngine:
    def __init__(self):
        self.board = chess.Board()
        self.learned_weights = self.load_weights()  # Tải trọng số học được

    def load_weights(self):
        """Tải trọng số học từ file, nếu không có thì dùng giá trị mặc định."""
        try:
            with open("chess_weights.pkl", "rb") as file:
                return pickle.load(file)
        except FileNotFoundError:
            return {"pawn": 100, "knight": 320, "bishop": 330, "rook": 500, "queen": 900}  # Trọng số mặc định

    def save_weights(self):
        """Lưu trọng số học vào file."""
        with open("chess_weights.pkl", "wb") as file:
            pickle.dump(self.learned_weights, file)

    def evaluate_board(self):
        """Hàm đánh giá trạng thái bàn cờ, dựa trên trọng số học được và các yếu tố khác."""
        material = sum(self.get_piece_value(piece) for piece in self.board.piece_map().values())
        control_center = self.control_center_score()
        mobility = self.mobility_score()
        return material + control_center + mobility

    def get_piece_value(self, piece):
        """Trả về giá trị của quân cờ dựa trên trọng số học được."""
        piece_type = piece.piece_type
        value = self.learned_weights.get(chess.PIECE_SYMBOLS[piece_type], 0)
        return value if piece.color == chess.WHITE else -value

    def control_center_score(self):
        """Đánh giá việc kiểm soát trung tâm."""
        center_squares = [chess.E4, chess.D4, chess.E5, chess.D5]
        score = 0
        for sq in center_squares:
            if self.board.piece_at(sq):
                score += self.get_piece_value(self.board.piece_at(sq))
        return score

    def mobility_score(self):
        """Đánh giá số lượng nước đi hợp lệ của các quân."""
        return len(list(self.board.legal_moves))

    def minimax(self, depth, alpha, beta, is_maximizing):
        """Thuật toán Minimax với cắt tỉa Alpha-Beta."""
        if depth == 0 or self.board.is_game_over():
            return self.evaluate_board()

        moves = list(self.board.legal_moves)
        if is_maximizing:
            max_eval = -float('inf')
            for move in moves:
                self.board.push(move)
                eval = self.minimax(depth - 1, alpha, beta, False)
                self.board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in moves:
                self.board.push(move)
                eval = self.minimax(depth - 1, alpha, beta, True)
                self.board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def get_best_move(self, depth=4):
        """Tìm nước đi tốt nhất với độ sâu tăng lên."""
        best_move = None
        best_value = -float('inf')
        for move in self.board.legal_moves:
            self.board.push(move)
            move_value = self.minimax(depth - 1, -float('inf'), float('inf'), False)
            self.board.pop()
            if move_value > best_value:
                best_value = move_value
                best_move = move
        return best_move

    def make_move(self, move):
        """Thực hiện nước đi."""
        if move in self.board.legal_moves:
            self.board.push(move)
            return True
        return False

    def update_weights(self, result):
        """Cập nhật trọng số dựa trên kết quả trận đấu."""
        if result == "1-0":  # Máy thua
            self.learned_weights["pawn"] += 1  # Tăng giá trị tốt
        elif result == "0-1":  # Máy thắng
            self.learned_weights["queen"] += 1  # Tăng giá trị hậu
        elif result == "1/2-1/2":  # Hòa
            self.learned_weights["knight"] += 1  # Tăng giá trị mã
        self.save_weights()  # Lưu lại trọng số sau mỗi trận đấu

    def self_play(self, games=10, depth=4):
        """Máy tự chơi với chính nó và học tập sau mỗi trận đấu."""
        for game in range(games):
            self.board.reset()
            while not self.board.is_game_over():
                best_move = self.get_best_move(depth)
                self.board.push(best_move)
            result = self.board.result()
            print(f"Trận {game + 1}: Kết quả {result}")
            self.update_weights(result)
        print("Tự học hoàn tất.")

    def play(self):
        """Chơi cờ với người dùng và học hỏi sau mỗi trận đấu."""
        game_count = 0
        while game_count < 4:
            self.board.reset()
            while not self.board.is_game_over():
                print(self.board)
                user_move = input("Nhập nước đi của bạn (ví dụ: e2e4): ")
                try:
                    move = chess.Move.from_uci(user_move)
                    if self.make_move(move):
                        best_move = self.get_best_move()
                        self.board.push(best_move)
                        print(f"Máy đi: {best_move}")
                    else:
                        print("Nước đi không hợp lệ, thử lại.")
                except ValueError:
                    print("Định dạng nước đi không hợp lệ, thử lại.")

            result = self.board.result()
            print(f"Trò chơi kết thúc với kết quả: {result}")
            self.update_weights(result)
            game_count += 1
            print(f"Đã hoàn thành {game_count} trận đấu. Lưu trọng số học...")

# Khởi tạo máy và cho tự chơi với chính nó
engine = ImprovedChessEngine()
engine.self_play(games=10, depth=1)  # Máy chơi 10 trận với chính nó để học
engine.play()  # Sau khi tự học, máy sẵn sàng chơi với người dùng
