import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, roc_curve, auc, precision_recall_curve, precision_score, recall_score, f1_score
from einops import reduce

"""
helper function to reduce the output classes to two classes
true: a list of true labels
prob: a list of predicted probabilities for each label, corresponding to true
data_labels: a list of data that the labels are stored in, corresponding to the order in prob
positive_label: label to choose as positive

ex. true = [1, 2, 0, 0]
    prob = [[0.1, 0.1, 0.8],
            [0.2, 0.3, 0.5],
            [0.8, 0.1, 0.1],
            [0.5, 0.4, 0.1]]
    data_labels = [0, 1, 2]
    show_labels = ['very good', 'good', 'bad']
    positive_label = 1

    return:
    true_result = [1, 0, 0, 0]
    prob_result = [0.1, 0.3, 0.1, 0.4]
    label = 'good'
"""
def reduce_to_two_classes(true, prob, data_labels, show_labels, positive_label):
    true_result = np.array(true)
    true_result = np.where(true_result == positive_label, 1, 0)

    # get the index of positive_labe in data_labels
    id = -1
    for index, label in enumerate(data_labels):
        if label == positive_label:
            id = index
            break
    if id == -1: raise Exception(f'{positive_label} does not exist in {data_labels}')

    prob_result = np.array(prob)
    prob_result = prob_result[:, index]

    return true_result.tolist(), prob_result.tolist(), show_labels[id]

"""
helper function for plotting confusion matrix
"""
def plot_confusion_matrix(true, pred, data_labels, show_labels):
    cm = confusion_matrix(true, pred, labels=data_labels)
    percentage = reduce(cm, 'a b -> a', 'sum')
    correct_predict = np.trace(cm)
    num_data = np.sum(cm)

    # Create figure and axes
    _, ax = plt.subplots()

    # Plot confusion matrix as an image
    im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)

    # Customize axes
    ax.set(xticks=np.arange(cm.shape[1]),
        yticks=np.arange(cm.shape[0]),
        xticklabels=show_labels,
        yticklabels=show_labels,
        xlabel='Predicted label',
        ylabel='True label')

    # Add percentage to each cell
    thresh = cm.max() / 2.0
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, f"{cm[i,j]} ({(100 * cm[i, j]) / percentage[i]:.2f}%)",
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")

    # Add a colorbar
    ax.figure.colorbar(im, ax=ax)

    # Adding accuracy at the upper left corner
    ax.text((cm.shape[1] - 1)/2, -0.8, f"accuracy = {correct_predict/num_data:.6f}", bbox=dict(facecolor='#87CEFA', edgecolor='black'), ha='center', va='center', color='black')

    return plt

"""
helper function for plotting ROC curve
"""
def plot_roc(true, prob, data_labels, show_labels, positive_label):
    true_result, prob_result, label = reduce_to_two_classes(true, prob, data_labels, show_labels, positive_label)
    # Compute the false positive rate, true positive rate, and thresholds
    fpr, tpr, _ = roc_curve(true_result, prob_result, pos_label=1)

    # Compute the area under the ROC curve (AUC)
    roc_auc = auc(fpr, tpr)

    # Plot the ROC curve
    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'positive = {label} (AUC = {roc_auc:.6f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc="lower right")
    
    return plt

"""
helper function for plotting PR curve
"""
def plot_pr(true, prob, data_labels, show_labels, positive_label):
    true_result, prob_result, label = reduce_to_two_classes(true, prob, data_labels, show_labels, positive_label)
    # Compute precision and recall values for class 1
    precision, recall, _ = precision_recall_curve(true_result, prob_result, pos_label=1)

    # Plot the PR Curve
    plt.plot(recall, precision, color='darkorange', label=f'positive = {label}')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve')
    plt.legend(loc="lower left")
    plt.grid(True)
    
    return plt

"""
helper function for plotting precision recall f1 graph
"""
def plot_prf(true, prob, data_labels, show_labels, positive_label):
    true_result, prob_result, label = reduce_to_two_classes(true, prob, data_labels, show_labels, positive_label)
    # Vary the threshold for prediction
    thresholds = np.linspace(0.0, 1.0, num=1000)

    precision_scores = []
    recall_scores = []
    f1_scores = []

    for threshold in thresholds:
        # Convert scores to binary predictions based on threshold
        binary_predictions = (np.array(prob_result) >= threshold).astype(int)

        # Compute precision, recall, and F1 scores
        precision = precision_score(true_result, binary_predictions, zero_division=np.nan)
        recall = recall_score(true_result, binary_predictions)
        f1 = f1_score(true_result, binary_predictions)

        precision_scores.append(precision)
        recall_scores.append(recall)
        f1_scores.append(f1)

    # Plot the graph
    plt.plot(thresholds, precision_scores, label='Precision')
    plt.plot(thresholds, recall_scores, label='Recall')
    plt.plot(thresholds, f1_scores, label='F1')
    plt.xlabel('Threshold')
    plt.ylabel('Score')
    plt.title(f'Precision, Recall, and F1 Scores (positive = {label})')
    plt.legend()
    plt.grid(True)
    
    return plt

plot_types = {"roc": (plot_roc, "roc_curve.png"),
              "pr": (plot_pr, "pr_curve.png"),
              "prf": (plot_prf, "precision_recall_f1.png")}