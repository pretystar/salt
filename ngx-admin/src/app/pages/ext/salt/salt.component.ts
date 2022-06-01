import { Component, Input, OnInit } from '@angular/core';
// import { NgForm } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { SaltInput, SaltService } from '../services/salt.service';

@Component({
  selector: 'ngx-salt',
  templateUrl: './salt.component.html',
  styleUrls: ['./salt.component.scss']
})

export class SaltComponent implements OnInit {
  // private saltsvc: SaltService
  minions: any
  data: any
  error: any
  @Input()  saltInput: SaltInput={target:'',fun:'test.ping',arg:'', isasync: false};
  
  constructor(private saltsvc: SaltService, private route: ActivatedRoute) {  }

  ngOnInit(): void { 
    const routeParams = this.route.snapshot.paramMap;
    this.saltInput.target=routeParams.get('target');

  }

  saltcmd(): void {
    console.log(this.saltInput)
    this.saltsvc.cmd(this.saltInput).subscribe(
      (data: any) => {
        console.log(data)
        this.minions = { ...data }
      }, // success path
      error => this.error = error // error path
    );
  }
}
