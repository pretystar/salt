import { ModuleWithProviders, NgModule, Optional, SkipSelf } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SaltComponent } from './salt/salt.component';
import { ExtRoutingModule } from './ext-routing.module';
import { SaltService } from './services/salt.service';
import { ExtComponent } from './ext.component';
import { Ng2SmartTableModule } from 'ng2-smart-table';
import { MatTableModule } from '@angular/material/table';
import {
  NbActionsModule,
  NbButtonModule,
  NbCardModule,
  NbCheckboxModule,
  NbDatepickerModule, NbIconModule,
  NbInputModule,
  NbRadioModule,
  NbSelectModule,
  NbUserModule,
} from '@nebular/theme';
import { ThemeModule } from '../../@theme/theme.module';
import { FormsModule as ngFormsModule } from '@angular/forms';
import { SaltminionsComponent } from './saltminions/saltminions.component';
@NgModule({
  declarations: [
    ExtComponent,
    SaltComponent,
    SaltminionsComponent
  ],
  imports: [
    CommonModule,
    ThemeModule,
    NbInputModule,
    NbCardModule,
    NbButtonModule,
    NbActionsModule,
    NbUserModule,
    NbCheckboxModule,
    NbRadioModule,
    NbDatepickerModule,
    NbSelectModule,
    NbIconModule,
    ngFormsModule,
    ExtRoutingModule,
    Ng2SmartTableModule,
    MatTableModule,
  ],
  providers: [
    SaltService,
  ],
})
export class ExtModule { 
  static forRoot(): ModuleWithProviders<ExtModule> {
    return {
      ngModule: ExtModule
    };
  }
}
