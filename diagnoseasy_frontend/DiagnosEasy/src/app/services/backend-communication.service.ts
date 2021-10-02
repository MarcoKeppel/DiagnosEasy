import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from "../../environments/environment";
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class BackendCommunicationService {

  public cf;

  constructor(
    public http: HttpClient,
  ) { }

  getInfo(): Observable<any> {

    let body = {
      'cf': this.cf
    };

    return this.http.post<any>(environment.apiUrl + 'ssn/get_info', JSON.stringify(body));
  }

  getCorrelations(info) {

    let body = {
      'info': info
    };

    return this.http.post<any>(environment.apiUrl + 'diagnoseasy/get_correlations', JSON.stringify(body));
  }
}
