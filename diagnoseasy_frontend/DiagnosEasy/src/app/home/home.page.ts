import { Component } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { Router } from '@angular/router';
import { BackendCommunicationService } from '../services/backend-communication.service';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage {

  cfForm = this.formBuilder.group({
    cf: '',
  });

  constructor(
    private router: Router,
    private formBuilder: FormBuilder,
    public backend: BackendCommunicationService,
  ) {}

  onSubmit(): void {

    let cf = this.cfForm.value.cf;
    console.log(cf);
    this.backend.cf = cf;
    this.router.navigate(['/results'], { state: { data: { cf: cf } } });
  }
}
