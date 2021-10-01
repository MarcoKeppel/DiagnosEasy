import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from "../../environments/environment";
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class BackendCommunicationService {

  constructor(
    public http: HttpClient,
  ) { }

  getInfo(cf: string): Observable<any> {

    let body = {
      'cf': cf
    };

    return this.http.post<any>(environment.apiUrl + 'ssn/get_cf', JSON.stringify(body));
  }

  getCorrelations(info) {

    let body = {
      'info': info
    };

    return this.http.post<any>(environment.apiUrl + 'ssn/get_correlations', JSON.stringify(body));
  }
}
