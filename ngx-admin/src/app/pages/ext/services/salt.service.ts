import { Injectable } from '@angular/core';
import { HttpClient,HttpErrorResponse  } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';
// import 'rxjs/add/operator/map';
// import 'rxjs/add/operator/filter';
export interface SaltInput {
  target: string;
  fun: string;
  arg: string;
  isasync: boolean;
}
@Injectable({
  providedIn: 'root'
})
export class SaltService {

  constructor(private http: HttpClient) { }
  
  //cmd({ target, func, arg, isasync }: { target; func; arg; isasync:false; }) : Observable<any>  {
  cmd(saltInput: SaltInput) : Observable<any>  {
    var data =  {"target": saltInput.target, "fun": saltInput.fun, "arg": saltInput.arg,"isasync": saltInput.isasync}

    return this.http.post("/salt/cmd", data).pipe(
      retry(3), // retry a failed request up to 3 times
      catchError(this.handleError) // then handle the error
    );
    
  }
  get_minions() : Observable<any> {
    return this.http.get("/salt/minions").pipe(
      retry(3), // retry a failed request up to 3 times
      catchError(this.handleError) // then handle the error
    );
  }
  get_grains(target='*') : Observable<any> {
    return this.http.get("/salt/grains/?target="+target).pipe(
      retry(3), // retry a failed request up to 3 times
      catchError(this.handleError) // then handle the error
    );
  }
  private handleError(error: HttpErrorResponse) {
    if (error.error instanceof ErrorEvent) {
      // A client-side or network error occurred. Handle it accordingly.
      console.error('An error occurred:', error.error.message);
    } else {
      // The backend returned an unsuccessful response code.
      // The response body may contain clues as to what went wrong,
      console.error(
        `Backend returned code ${error.status}, ` +
        `body was: ${error.error}`);
    }
    // return an observable with a user-facing error message
    return throwError(
      'Something bad happened; please try again later.');
  };
//   public 
}
