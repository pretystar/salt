import { Component, OnInit } from '@angular/core';
import { SaltService } from '../services/salt.service';
@Component({
  selector: 'ngx-saltjoblist',
  templateUrl: './saltjoblist.component.html',
  styleUrls: ['./saltjoblist.component.scss']
})
export class SaltjoblistComponent implements OnInit {
  data = null;
  error = null;
  displayedColumns: string[] = ['id', 'user', 'function', 'target', 'starttime','actions'];

  constructor(private saltsvc: SaltService) { }

  ngOnInit(): void {
    this.saltsvc.get_jobs("").subscribe((data: any) => {
      this.data = data

    },
    error => {this.error = error} // error path)
    )
  }

}
