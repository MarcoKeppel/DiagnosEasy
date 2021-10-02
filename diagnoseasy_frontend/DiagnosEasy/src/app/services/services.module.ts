import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BackendCommunicationService } from './backend-communication.service';



@NgModule({
  declarations: [
    BackendCommunicationService,
  ],
  imports: [
    CommonModule,
  ]
})
export class ServicesModule { }
