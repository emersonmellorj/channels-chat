
// Recebendo valores do python em propriedades criadas na tag Body

const nome_sala = document.getElementById("corpo").getAttribute("data-sala");
const usuario = document.getElementById("corpo").getAttribute("data-username");
const perfil_image = document.getElementById("corpo").getAttribute("data-image")
var status = '';

$(".messages").animate({ scrollTop: $(document).height() }, "fast");

$("#profile-img").click(function() {
    const status = document.querySelector("#status-options")

    if(status.className === "active"){
        $("#status-options").removeClass("active");
        return;
    } else{
        $("#status-options").addClass("active");
        return;
    }
});

$(".expand-button").click(function() {
    $("#profile").toggleClass("expanded");
    $("#contacts").toggleClass("expanded");
});

$("#status-options ul li").click(function() {
    $("#profile-img").removeClass();
    $("#status-online").removeClass("active");
    $("#status-away").removeClass("active");
    $("#status-busy").removeClass("active");
    $("#status-offline").removeClass("active");
    $(this).addClass("active");
    
    if($("#status-online").hasClass("active")) {
        $("#profile-img").addClass("online");
        $("#status-online").addClass("active");
        status = 'online';
    } else if ($("#status-away").hasClass("active")) {
        $("#profile-img").addClass("away");
        $("#status-away").addClass("active");
        status = 'away';
    } else if ($("#status-busy").hasClass("active")) {
        $("#profile-img").addClass("busy");
        $("#status-busy").addClass("active");
        status = 'busy';
    } else if ($("#status-offline").hasClass("active")) {
        $("#profile-img").addClass("offline");
        $("#status-offline").addClass("active");
        status = 'offline';
    } else {
        $("#profile-img").removeClass();
        status = '';
    };

    // Preciso chamar uma view para atualizar o valor do status na tabela LoggedUser
    var csrf_token = document.querySelector("#token").value;
    $(function(){
        $.ajax({
            url: "status",
            type: "get",
            data: {
                status: status,
                csrf_token: csrf_token
            },
            success: function(){
                //console.log('Atualizacao realizada com sucesso!')
            }
        });
    });
    
    $("#status-options").removeClass("active");
});


function newMessage() {

    message = $(".message-input input").val();
    if($.trim(message) == '') {
        return false;
    }
    
    chatSocket.send(JSON.stringify({
        'mensagem': message
    }));
    
    $('.message-input input').val(null);
    $('.contact.active .preview').html('<span>Você: </span>' + message);
    $(".messages").animate({ scrollTop: $(document).height() }, "fast");
    
};


// Passando a classe active para o status-online correto (bolinha que marca o status do usuario)
var status_bolinha = document.querySelector("#status-options").getAttribute("data-status");

if(status_bolinha === "online"){
    $("#status-online").addClass("active")
}else if(status_bolinha === "away"){
    $("#status-away").addClass("active")
}else if(status_bolinha === "busy"){
    $("#status-busy").addClass("active")
}else{
    $("#status-offline").addClass("active")
}


// Criando o socket
const chatSocket = new WebSocket(
    'ws://' + window.location.host + 
    '/ws/chat/' + nome_sala + '/'
);

chatSocket.onmessage = function(event) {
    const dados = JSON.parse(event.data);
    // const usuario = "{{request.user.username}}";
    const mensagem = dados["mensagem"];
    const author = dados['author'];
    console.log(author)

    var data = new Date();
    h=data.getHours();
    m=data.getMinutes();
    s=data.getSeconds();
    var hora_local = h + ":" + m + ":" + s
    console.log(hora_local);
    
    if(author === usuario){
        $('<li class="sent"><img src="' + perfil_image + '" alt="" /><p>' + 
            mensagem + '<br><span>' + hora_local + '</span></p></li>').appendTo($('.messages ul'));
        $('.contact.active .preview').html('<span>Você: </span>' + message);
        $(".messages").animate({ scrollTop: $(document).height() }, "fast");
            
    } else {

        // Resgatando a foto do outro usuario que mandou a mensagem no chat
        const other_user_chat = author
        $(function(){
            $.ajax({
                url: "get_image_other_user",
                type: "get",
                data: {
                    other_user_chat: other_user_chat,
                },
                success: function(other_user_image){
                    $('<li class="replies"><img src="'+ other_user_image +'" alt="" /><p>' + 
                        mensagem + '<br><span>' + hora_local + '</span></p></li>').appendTo($('.messages ul'));
                    console.log('Resgate da foto de perfil realizada com sucesso!')
                }
            });
        });

        $(".messages").animate({ scrollTop: $(document).height() }, "fast");
        
    }
    
};

document.querySelector('.message-input input').onkeypress = function(event) {
    if(event.keyCode === 13) {
        document.querySelector('#botao').click();
    }
};

document.querySelector('#botao').onclick = function(event) {
    const mensagemInput = document.querySelector('.message-input input');
    newMessage();
    mensagemInput.value = '';
};

//# sourceURL=pen.js