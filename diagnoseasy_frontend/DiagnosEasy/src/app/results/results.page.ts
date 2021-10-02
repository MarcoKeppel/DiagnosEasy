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
         let obj = JSON.parse("{}");
         let diabetes_data = JSON.parse(obj.info_diabetes);
         let info_coronary_heart_disease_data = JSON.parse(obj.info_coronary_heart_disease);
         let diabetes_percentile = obj.diabetes;
         let heart_disease = obj.coronary_heart_disease;

       });
     });
  }

  toggleCard(index: number){
    this.openCards[index] = ! this.openCards[index];
  }


}
