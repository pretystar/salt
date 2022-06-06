import { Component, Input, OnInit, ViewChild  } from '@angular/core';
import { SaltInput, SaltService } from '../services/salt.service';
import { SmartTableData } from '../../../@core/data/smart-table';
import { LocalDataSource } from 'ng2-smart-table';
import { MatTableModule } from '@angular/material/table';
import { DialogComponent } from '../../modal-overlays/dialog/dialog.component';
import {MatDialog, MatDialogRef, MAT_DIALOG_DATA} from '@angular/material/dialog';
// import {MatDialogModule} from '@angular/material/dialog';

import { JsondialogComponent } from '../jsondialog/jsondialog.component';
@Component({
  selector: 'ngx-saltminions',
  templateUrl: './saltminions.component.html',
  styleUrls: ['./saltminions.component.scss']
})
export class SaltminionsComponent implements OnInit {
  data: any
  error: any
  minions = []
  
  displayedColumns: string[] = ['id', 'fqdn', 'osfinger', 'details', 'actions'];

  constructor(private saltsvc: SaltService, public dialog: MatDialog){}
  
  ngOnInit(): void {
    this.get_grains()
  }
  
  get_minion(){
    this.saltsvc.get_minions().subscribe((data: any) => {
      this.data = { ...data }
      var upminions = [...data.up]
      // var minions = { ...upminions }
      // console.log(minions)
      upminions.forEach(element => {
        console.log(element)
        this.saltsvc.get_grains(element).subscribe((data: any) => {
          this.minions.push(data)
        }
        )
      });
    }, // success path
    error => {this.error = error} // error path)
    )
  }
  showdetails(element){
    console.log(element)
    const dialogRef = this.dialog.open(JsondialogComponent, {
      width: '250px',
      data: element,
    });
    dialogRef.afterClosed().subscribe(result => {
      console.log(`Dialog result: ${result}`);
    });
  }
  // runcmd(element){
  //   console.log(element)
  //   const dialogRef = this.dialog.open(JsondialogComponent, {
  //     width: '250px',
  //     data: element,
  //   });
  //   dialogRef.afterClosed().subscribe(result => {
  //     console.log(`Dialog result: ${result}`);
  //   });
  // }
  get_grains(){
    this.saltsvc.get_grains().subscribe((data: any) => {
      this.data = data
      // Object.entries(data).forEach(item => {
      //   this.minions.push(item)
      // })
    },
    error => {this.error = error} // error path)
    )
  }
}
// @Component({
//   selector: 'json-dialog',
//   template: '<ngx-jsondialog [data]="data"></ngx-jsondialog>',
// })

// export class JsonDialog {
//   @ViewChild(JsondialogComponent) editor: JsondialogComponent;

//   constructor() { 
//     // this.editorOptions.modes = ['code', 'text', 'tree', 'view']; // set all allowed modes
//     //this.options.mode = 'code'; //set only one mode
      
//       // this.data = {"products":[{"name":"car","product":[{"name":"honda","model":[{"id":"civic","name":"civic"},{"id":"accord","name":"accord"},{"id":"crv","name":"crv"},{"id":"pilot","name":"pilot"},{"id":"odyssey","name":"odyssey"}]}]}]}
//   }

// }