import { Component, ViewChild  } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { LoadingController, AlertController, IonContent  } from '@ionic/angular';


@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})

export class HomePage {
  text: String
  final: String
  response: any
  show_results: boolean

  message: String

  constructor(private http: HttpClient, public loadingController: LoadingController, public alertController: AlertController) {
    this.text = ""
    this.final = ""
    this.response = null
    this.show_results = false

    this.message = ""
  }

  get_message(fake, proba) {

    let result = fake == 1 ? "falsa" : "verdadeira"

    let phrases = [
      `Tenho ${proba}% de certeza de que essa notícia é ${result}.`,
      `Tenho uma confiança de ${proba}% de que essa notícia é ${result}.`,
      `Essa notícia é ${result} com ${proba}% de certeza.`,
      `Há uma chance de ${proba}% de que essa notícia seja ${result}.`,
      `Essa notícia tem ${proba}% de chance de ser ${result}.`
    ]

    let x = Math.floor(Math.random() * (phrases.length))

    let message = phrases[x]

    message += " Sempre procure por outras fontes confiáveis!"
    
    return message
  }

  enviar() {

    this.final = ""
    this.response = null

    let normalizedString = this.text.normalize("NFD").replace(/[\u0300-\u036f]/g, "")

    let stringTest = normalizedString.toLowerCase().replace(/[^a-zA-Z ]/gi, ' ').replace(/\s{2,}/gi, ' ').trim()
    
    if(stringTest.split(' ').length < 20) {
      this.show_results = true
      this.message = "Insira uma notícia com 20 ou mais caracteres!"
      return
    }



    let controller = this.loadingController
    controller.create({ 
      message: 'Processando notícia'
    }).then(loading => loading.present());

    this.http.post('http://hiideaki.pythonanywhere.com/classification', {text: this.text}).subscribe((response) => {
      console.log(response)
      this.show_results = true
      this.response = response
      this.final = this.response.results.pred == 1 ? "falsa" : "verdadeira"
      this.message = this.get_message(this.response.results.pred, this.response.results.proba)
      // this.message = "Tenho " + this.response.results.proba + "% de certeza de que esta notícia é " +  this.final + "."
      controller.dismiss()
    },
    (err) => {
      this.show_results = true
      this.message = "Opa! Ocorreu um erro! Pedimos desculpas pelo inconveniente."
      controller.dismiss()
    })
  }

  async limpar() {

    const controller = await this.alertController.create({
      header: 'Limpar',
      message: 'Deseja descartar a notícia atual?',
      buttons: [
        {
          text: 'Cancelar',
          role: 'cancel'
        }, {
          text: 'Sim',
          handler: () => {
            this.message = ""
            this.text = ""
            this.show_results = false
            this.final = ""
            this.response = null
          }
        }
      ]
    })

    await controller.present()
    
  }

}
