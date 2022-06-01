import { Component, Input, OnInit, ViewChild  } from '@angular/core';
import { SaltInput, SaltService } from '../services/salt.service';
import { SmartTableData } from '../../../@core/data/smart-table';
import { LocalDataSource } from 'ng2-smart-table';
import { MatTableModule } from '@angular/material/table';
import { DialogComponent } from '../../modal-overlays/dialog/dialog.component';
import { MatDialog } from '@angular/material/dialog';
@Component({
  selector: 'ngx-saltminions',
  templateUrl: './saltminions.component.html',
  styleUrls: ['./saltminions.component.scss']
})
export class SaltminionsComponent implements OnInit {
  data: any
  error: any
  minions = []
  
  // source1: LocalDataSource = new LocalDataSource();

  displayedColumns: string[] = ['id', 'fqdn', 'osfinger', 'details', 'actions'];

  // constructor(private service: SmartTableData) {
  //   const data = this.service.getData();
  //   this.source.load(data);
  // }
  // constructor(private saltsvc: SaltService, private table: SmartTableData) { 
  //   const data = this.table.getData();
  //   this.source1.load(data);
  // }
  constructor(private saltsvc: SaltService, public dialog: MatDialog){}
  // settings = {
  //   add: {
  //     addButtonContent: '<i class="nb-plus"></i>',
  //     createButtonContent: '<i class="nb-checkmark"></i>',
  //     cancelButtonContent: '<i class="nb-close"></i>',
  //   },
  //   edit: {
  //     editButtonContent: '<i class="nb-edit"></i>',
  //     saveButtonContent: '<i class="nb-checkmark"></i>',
  //     cancelButtonContent: '<i class="nb-close"></i>',
  //   },
  //   delete: {
  //     deleteButtonContent: '<i class="nb-trash"></i>',
  //     confirmDelete: true,
  //   },
  //   columns: {
  //     id: {
  //       title: 'id',
  //       type: 'id',
  //     },
  //     fqdn: {
  //       title: 'fqdn',
  //       type: 'fqdn',
  //     },
  //     firstName: {
  //       title: 'osfinger',
  //       type: 'osfinger',
  //     }
  //   },
  // };
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
  }
  runcmd(element){
    console.log(element)
    // const dialogRef = this.dialog.open(JsonDialog, element.value);

    // dialogRef.afterClosed().subscribe(result => {
    //   console.log(`Dialog result: ${result}`);
    // });
  }
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
//   template: '<json-editor [options]="editorOptions" [data]="data"></json-editor>',
// })

// export class JsonDialog {
//   @Input() data;
//   public editorOptions: JsonEditorOptions;
//   @ViewChild(JsonEditorComponent) editor: JsonEditorComponent;

//   constructor() { 
//     this.editorOptions = new JsonEditorOptions()
//     this.editorOptions.modes = ['code', 'text', 'tree', 'view']; // set all allowed modes
//     //this.options.mode = 'code'; //set only one mode
      
//       // this.data = {"products":[{"name":"car","product":[{"name":"honda","model":[{"id":"civic","name":"civic"},{"id":"accord","name":"accord"},{"id":"crv","name":"crv"},{"id":"pilot","name":"pilot"},{"id":"odyssey","name":"odyssey"}]}]}]}
//   }

// }