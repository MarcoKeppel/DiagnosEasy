import { Component, OnInit } from '@angular/core';
import { BackendCommunicationService } from '../services/backend-communication.service';
import { Platform } from '@ionic/angular';

@Component({
  selector: 'app-results',
  templateUrl: './results.page.html',
  styleUrls: ['./results.page.scss'],
})
export class ResultsPage implements OnInit {

  pageIsReady = true;
  results = [];
  openCards = [false];
  name : string;
  birthday : string;
  gender: string

  constructor(
    public platform: Platform,
    public backend: BackendCommunicationService,
  ) { }

  ngOnInit() {
     this.backend.getInfo().subscribe(info => {

       this.backend.getCorrelations(info).subscribe(result => {

         this.results = result;

         this.pageIsReady = true;
         console.log(this.results)
         console.log(this.results["info_coronary_heart_disease"]["Firstname"])
         this.name = this.results["info_coronary_heart_disease"]["Firstname"] + " " + this.results["info_coronary_heart_disease"]["Lastname"]
         this.birthday = this.results["info_coronary_heart_disease"]["Day of birth"];
         this.gender = this.results["info_coronary_heart_disease"]["Gender"];
         //let diabetes_data = JSON.parse(obj.info_diabetes);
         //let info_coronary_heart_disease_data = JSON.parse(obj.info_coronary_heart_disease);
         //let diabetes_percentile = obj.diabetes;
         //let heart_disease = obj.coronary_heart_disease;

       });
     });
  }

  toggleCard(index: number){
    this.openCards[index] = ! this.openCards[index];
  }


}
