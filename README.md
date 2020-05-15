## Projeto que desenvolve uma aplicação em tempo real - um Chat

- Estamos utilizando channels, routing, consumers e async / await nas funcoes.

- Utilizamos o bootstrap4 como um pacote instalado no django

    {% load bootstrap4 %}

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <title>Geek Chat</title>
        {% bootstrap_css %}
    </head>
    <body>
        <div class="container">
            Qual sala de chat você gostaria de entrar?<br/>
            <input id="nome_sala" name="nome_sala" type="text" size="100" placeholder="Nome da sala ..."><br/>
            {% buttons %}
                <input id="botao" class="btn btn-primary" type="button" value="Entrar">
            {% endbuttons %}
        </div>
        {% bootstrap_javascript jquery='full' %}

        <script>

            document.querySelector('#nome_sala').focus();
            document.querySelector('#nome_sala').onkeyup = function(event) {
                if(event.KeyCode==13){
                    document.querySelector('#botao').click();
                }
            };

            document.querySelector("#botao").onclick = function(event) {
                const nome_sala = document.querySelector('#nome_sala').value();
                if(nome_sala != ""){
                    window.location.pathname = '/chat/' + nome_sala + '/';
                }
                else {
                    alert('Você precisa informar o nome da sala!');
                    document.querySelector('#nome_sala').focus();
                }
            };
            
        </script>
    </body>
    </html>

- 