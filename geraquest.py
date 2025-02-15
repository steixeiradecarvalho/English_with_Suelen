import re
from typing import List, Dict

class ExerciseTemplate:
    def __init__(
        self,
        title: str,
        instructions: str,
        tip: str,
        questions: List[Dict[str, str]]
    ):
        self.title = title
        self.instructions = instructions
        self.tip = tip
        self.questions = questions
        
    def _generate_questions_html(self) -> tuple[str, str, dict]:
        questions_html = []
        answers_dict = {}
        
        for idx, q in enumerate(self.questions, 1):
            # Replace ___ with input field
            question_text = q['question']
            gap_count = question_text.count('___')
            
            for gap_idx in range(gap_count):
                input_id = f'q{idx}_{gap_idx + 1}' if gap_count > 1 else f'q{idx}'
                question_text = question_text.replace('___', f'<input type="text" id="{input_id}">', 1)
                answers_dict[input_id] = q['answers'][gap_idx]
            
            # Create question HTML with translation
            question_html = f'''
                <div class="question">
                    {question_text}
                    <div class="translation-container">
                        <i class="fas fa-language translation-icon" tabindex="0"></i>
                        <span class="translation">{q['translation']}</span>
                    </div>
                </div>'''
            questions_html.append(question_html)
        
        # Create JavaScript answers object
        answers_js = "{\n" + ",\n".join(
            f'            {k}: "{v}"' for k, v in answers_dict.items()
        ) + "\n        }"
        
        return ("\n".join(questions_html), answers_js, answers_dict)

    def generate_html(self) -> str:
        questions_html, answers_js, _ = self._generate_questions_html()
        
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.title}</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        /* General Styles */
        body {{
            font-family: 'Arial', sans-serif;
            background-color: #f8f9fa;
            color: #343a40;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
            margin: 0;
        }}

        .container {{
            max-width: 800px;
            margin: 20px auto;
            padding: 20px;
            flex: 1;
        }}

        h1, h2, h3 {{
            color: #007bff;
        }}

        /* Exercise Styles */
        .exercise-box {{
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }}

        .question {{
            margin-bottom: 15px;
            position: relative;
        }}

        select, input[type="text"] {{
            padding: 8px;
            margin: 0 5px;
            border: 1px solid #ced4da;
            border-radius: 5px;
            transition: border-color 0.3s;
        }}

        .results {{
            margin-top: 20px;
            padding: 15px;
            border-radius: 5px;
            display: none;
            background-color: #f2f2f2;
        }}

        .correct {{
            color: #28a745;
        }}

        .incorrect {{
            color: #dc3545;
        }}

        .example {{
            color: #6c757d;
            font-style: italic;
            margin-bottom: 10px;
        }}

        /* Translation styles */
        .translation-container {{
            display: inline-block;
            position: relative;
            margin-left: 10px;
        }}

        .translation {{
            display: none;
            position: absolute;
            top: 100%;
            left: 0;
            background-color: #f8f9fa;
            border: 1px solid #ced4da;
            border-radius: 5px;
            padding: 5px 10px;
            margin-top: 5px;
            color: #6c757d;
            font-style: italic;
            white-space: nowrap;
            z-index: 100;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}

        .translation-icon {{
            cursor: pointer;
            color: #007bff;
            margin-left: 10px;
        }}
        
        button {{
            background-color: #007bff;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s;
        }}

        button:hover {{
            background-color: #0056b3;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="exercise-box">
            <h2>{self.title}</h2>
            <p>{self.instructions}</p>
            <p>(Clique no ícone ao lado da frase, para tradução)</p>
            
            <div class="example"><u>Dica:</u><br> {self.tip}</div>
            
            <div id="questions">
                {questions_html}
            </div>
    
            <button onclick="checkAnswers()">Check answers</button>
            
            <div id="result" class="results"></div>
        </div>
    </div>
    <script>
        const correctAnswers = {answers_js};
        
        function checkAnswers() {{
            let score = 0;
            const totalQuestions = Object.keys(correctAnswers).length;
            
            for (const questionId in correctAnswers) {{
                const userAnswer = document.getElementById(questionId).value.trim().toLowerCase();
                const correctAnswer = correctAnswers[questionId];
                const questionElement = document.getElementById(questionId).parentElement;

                if (userAnswer === correctAnswer) {{
                    score++;
                    questionElement.classList.add('correct');
                    questionElement.classList.remove('incorrect');
                }} else {{
                    questionElement.classList.add('incorrect');
                    questionElement.classList.remove('correct');
                }}
            }}

            const resultDiv = document.getElementById('result');
            resultDiv.style.display = 'block';
            //XXX
            resultDiv.innerHTML = `
                <h3>Your result: ${{score}}/${{totalQuestions}}</h3>
                <p>Correct answers:</p>
                <ul>
                    ${{Object.entries(correctAnswers).map(([id, answer]) => {{
                        const questionText = document.getElementById(id).parentElement.textContent.trim()
                            .replace(/\\s+/g, ' ')
                            .split(/fa-language/)[0];
                        return `<li>${{questionText.trim()}} → <strong>${{answer}}</strong></li>`;
                    }}).join('')}}
                </ul>
            `;
            /XXX
        }}

        // Initialize translation handlers
        document.addEventListener('DOMContentLoaded', function() {{
            const translationIcons = document.querySelectorAll('.translation-icon');
            
            translationIcons.forEach(icon => {{
                function showTranslation() {{
                    const translation = icon.nextElementSibling;
                    if (translation) translation.style.display = 'block';
                }}
                
                function hideTranslation() {{
                    const translation = icon.nextElementSibling;
                    if (translation) translation.style.display = 'none';
                }}
                
                icon.addEventListener('mousedown', function(e) {{
                    e.preventDefault();
                    showTranslation();
                }});
                
                icon.addEventListener('mouseup', hideTranslation);
                icon.addEventListener('mouseleave', hideTranslation);
                
                icon.addEventListener('keydown', function(e) {{
                    if (e.key === 'Enter' || e.key === ' ') {{
                        e.preventDefault();
                        showTranslation();
                    }}
                }});
                
                icon.addEventListener('keyup', function(e) {{
                    if (e.key === 'Enter' || e.key === ' ') {{
                        hideTranslation();
                    }}
                }});
                
                icon.addEventListener('touchstart', function(e) {{
                    e.preventDefault();
                    showTranslation();
                }}, {{ passive: false }});
                
                icon.addEventListener('touchend', hideTranslation);
                icon.addEventListener('touchcancel', hideTranslation);
            }});
        }});
    </script>
</body>
</html>'''

def main():
    # Example usage
    exercise_data = {
        'title': 'Simple Present',
        'instructions': 'Complete the sentences with the correct form of the verbs in parentheses.',
        'tip': 'For He/She/It, add -s to the base form of the verb.',
        'questions': [
            {
                'question': 'She ___ in London (live)',
                'translation': 'Ela mora em Londres',
                'answers': ['lives']
            },
            {
                'question': 'They ___ shrimp (eat)',
                'translation': 'Eles comem camarão',
                'answers': ['eat']
            }
        ]
    }
    
    template = ExerciseTemplate(
        title=exercise_data['title'],
        instructions=exercise_data['instructions'],
        tip=exercise_data['tip'],
        questions=exercise_data['questions']
    )
    
    # Generate HTML and save to file
    html_content = template.generate_html()
    with open('exerc.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == '__main__':
    main()
