# The Quiz Union
hosted at: https://quiz-union.herokuapp.com

A quiz website that fetches questions from the Open Trivia API.
Admin users can also add questions to the databse

# Features
<ul>
  <li>User can configure the category and difficulty of questions to be shown.</li>
  
  <li>The Quiz Union fetches <b>questions</b> and <b>categories</b> from both- the <a href="https://opentdb.com/api_config.php">Open Trivia API</a>, and those that were custom added to the database.</li>

  <li>You have your very own <a href="{% url 'users:profile' %}">profile</a> dashboard, wherein you can find your <b>quiz history</b> and revisit them and their results.</li>

  <li>Although not required, you can <a href="{% url 'update_categories' %}">refresh</a> the quiz categories to fetch the most up-to-date categories from Open Trivia.</li>
  
  <li><b>Inbuilt-timer</b> to time your responses.</li>
  <li>run <b>python manage.py test</b> to run tests.</li>
</ul>
