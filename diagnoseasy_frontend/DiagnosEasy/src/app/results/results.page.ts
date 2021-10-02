import { Component, OnInit } from '@angular/core';
import { BackendCommunicationService } from '../services/backend-communication.service';

@Component({
  selector: 'app-results',
  templateUrl: './results.page.html',
  styleUrls: ['./results.page.scss'],
})
export class ResultsPage implements OnInit {

  pageIsReady = false;
  results = [];

  constructor(
    public backend: BackendCommunicationService,
  ) { }

  ngOnInit() {

    this.backend.getInfo().subscribe(info => {

      this.backend.getCorrelations(info).subscribe(result => {

        this.results = result;

        this.pageIsReady = true;

      });
    });
  }

}
