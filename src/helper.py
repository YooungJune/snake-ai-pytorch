import matplotlib.pyplot as plt
import matplotlib
import os
matplotlib.use('Agg')  # 使用非交互后端，避免线程问题

def plot(scores, mean_scores):
    """绘制训练曲线，保存为图片而不是实时显示"""
    try:
        plt.figure(figsize=(10, 5))
        plt.clf()
        plt.title('Training Progress')
        plt.xlabel('Number of Games')
        plt.ylabel('Score')
        plt.plot(scores, label='Score', alpha=0.7)
        plt.plot(mean_scores, label='Mean Score', alpha=0.7)
        plt.ylim(ymin=0)
        
        if len(scores) > 0:
            plt.text(len(scores)-1, scores[-1], str(scores[-1]), fontsize=9)
        if len(mean_scores) > 0:
            plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]), fontsize=9)
        
        plt.legend()
        plt.tight_layout()
        
        # 保存而不是显示，避免线程问题
        progress_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'model', 'training_progress.png')
        os.makedirs(os.path.dirname(progress_path), exist_ok=True)
        plt.savefig(progress_path, dpi=80, bbox_inches='tight')
        plt.close()
    except Exception as e:
        print(f"绘图错误: {e}")
        plt.close()

