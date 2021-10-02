import { Component, OnInit } from '@angular/core';
import { BackendCommunicationService } from '../services/backend-communication.service';
import { Platform } from '@ionic/angular';
import { Router } from '@angular/router';

@Component({
  selector: 'app-results',
  templateUrl: './results.page.html',
  styleUrls: ['./results.page.scss'],
})
export class ResultsPage implements OnInit {

  pageIsReady = false;
  results = [];
  openCards = [false, false];
  name : string;
  birthday : string;
  gender: string
  age : number
  diabetes_likelyhood : number
  day_of_birth : string
  blood_preassure_medicine : string
  HDL_choleserol : number
  smoker : string
  systolic_bp : number
  total_cholesterol : number
  coronary_heart_disease_likelyhood : number
  bmi : number
  family_history : string
  antihypertensive_medication: string
  prescribed_steroids : string
  smoking_history : string

  constructor(
    public platform: Platform,
    public router: Router,
    public backend: BackendCommunicationService,
  ) { }

  ngOnInit() {}
  ionViewWillEnter() {

    if (this.backend.cf == null) {
      this.router.navigate(['/']);
      return;
    }

     this.backend.getInfo().subscribe(info => {

       this.backend.getCorrelations(info).subscribe(result => {

         this.results = result;


         console.log(this.results)

         this.name = this.results["info_coronary_heart_disease"]["Firstname"] + " " + this.results["info_coronary_heart_disease"]["Lastname"]

         this.age = this.results["info_coronary_heart_disease"]["Age"];
         this.birthday = this.results["info_coronary_heart_disease"]["Day of birth"];
         this.gender = this.results["info_coronary_heart_disease"]["Sex"];
         this.day_of_birth = this.results["info_coronary_heart_disease"]["Day of birth"];
         this.blood_preassure_medicine = this.results["info_coronary_heart_disease"]["Blood pressure being treated with medicines"];
         this.HDL_choleserol = this.results["info_coronary_heart_disease"]["HDL cholesterol mg/dL"];
         this.smoker = this.results["info_coronary_heart_disease"]["Smoker"];
         this.systolic_bp = this.results["info_coronary_heart_disease"]["Systolic BP mm Hg"];
         this.systolic_bp = Math.round(this.systolic_bp * 100) / 100;
         this.total_cholesterol = this.results["info_coronary_heart_disease"]["Total cholesterol mg/dL"];
         this.total_cholesterol = Math.round(this.total_cholesterol * 100) / 100;

         this.diabetes_likelyhood = this.results["diabetes"] / 100
         this.coronary_heart_disease_likelyhood = this.results["coronary_heart_disease"] / 100;
         this.bmi = this.results["info_diabetes"]["BMI kg/m^2"];
         this.family_history = this.results["info_diabetes"]["Family history"];
         this.antihypertensive_medication = this.results["info_diabetes"]["Prescribed antihypertensive medication"];
         this.prescribed_steroids = this.results["info_diabetes"]["Prescribed steroids"];
         this.smoking_history = this.results["info_diabetes"]["Smoking history"];

         this.pageIsReady = true;
       });
     });
  }

  toggleCard(index: number){
    this.openCards[index] = ! this.openCards[index];
  }


}
