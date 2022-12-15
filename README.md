# Image-Reconstruction-CGNR-CGNE
Projeto desenvolvido para a disciplina de Desenvolvimento Integrado de Sistemas.

http://127.0.0.1:8000/api/request/      #Cria um registro direto na tabela
Json de exemplo:
{
  "user_id": 100,
  "user_name": "vitor",
  "image": "sdadasds.bmp",
  "image_pixel_size": 100,
  "algorithm_name": "cgnr",
  "iterations": 28
}

http://127.0.0.1:8000/api/return_requests/    #Retorna uma lista de Json de todos os registros na tabela
http://127.0.0.1:8000/api/return_requests/1   #Retorna um registro específico (passando o ID)

http://127.0.0.1:8000/api/return_image/1      #Retorna o caminho da imagem e realiza um plot da imagem (passando o ID do registro)

http://127.0.0.1:8000/api/generate_images/    #Realiza a reconstrução das imagens conforme sinal e algoritmo informado, enviado em forma de lista (pode ser mais de 1 registro)
                                              #Os valores do "algorithm" podem ser ("cgnr","cgne")
                                              #Os valores do "signal_name" podem ser ("30x30-1", "30x30-2", "60x60-1", "60x60-2")
Json de exemplo:
[
{
  "user_id": 8,
  "user_name": "vitor8",
  "algorithm": "cgnr",
  "signal_name": "30x30-1"
},
{
  "user_id": 9,
  "user_name": "vitor9",
  "algorithm": "cgnr",
  "signal_name": "30x30-2"
},
{
  "user_id": 10,
  "user_name": "vitor10",
  "algorithm": "cgnr",
  "signal_name": "60x60-1"
},
{
  "user_id": 11,
  "user_name": "vitor11",
  "algorithm": "cgnr",
  "signal_name": "60x60-2"
}
]
