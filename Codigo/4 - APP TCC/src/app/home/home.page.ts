import { Component } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { LoadingController } from '@ionic/angular';


@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})

export class HomePage {

  text: String
  final: String
  response: any
  sent_request: boolean

  message: String

  constructor(private http: HttpClient, public loadingController: LoadingController) {
    this.text = ""
    this.final = ""
    this.response = null
    this.sent_request = false

    this.message = ""
  }

  enviar() {
    this.final = ""
    this.response = null

    let controller = this.loadingController
    controller.create({ 
      message: 'Processando notícia'
    }).then(loading => loading.present());

    this.http.post('http://hiideaki.pythonanywhere.com/classification', {text: this.text}).subscribe((response) => {
      console.log(response)
      this.sent_request = true
      this.response = response
      this.final = this.response.results.pred == 1 ? "falsa" : "verdadeira"
      this.message = "Tenho " + this.response.results.proba + "% de certeza de que esta notícia é " +  this.final + "."
      controller.dismiss()
    },
    (err) => {
      this.sent_request = true
      this.message = "Erro " + err.status + ": " + err.statusText
      controller.dismiss()
    })
  }

}
