import { Component } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';


@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})

export class HomePage {

  text: String
  response: any
  error: any

  constructor(private http: HttpClient) {
    
    this.text = 'Insira a notícia aqui!'
    this.response = null
  }

  enviar() {

    // this.http.get('http://localhost:8000/test').subscribe((response) => {
    //   this.error = response
    //   // this.response = response
    // },
    // (err) => {
    //   this.error = err.headers
    // });

    this.http.post('http://localhost:8000/inference', {text: this.text}).subscribe((response) => {
      alert('Success: ' + response)
      this.response = response
    },
    (err) => {
      alert('Error: ' + err.message)
    });
  }

}
