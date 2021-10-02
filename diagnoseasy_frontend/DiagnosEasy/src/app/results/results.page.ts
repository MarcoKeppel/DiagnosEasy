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
    // this.backend.getInfo().subscribe(info => {
    //
    //   this.backend.getCorrelations(info).subscribe(result => {
    //
    //     this.results = result;
    //
    //     this.pageIsReady = true;
    //
    //   });
    // });
  }

  toggleCard(index: number){
    this.openCards[index] = ! this.openCards[index];
  }


}
